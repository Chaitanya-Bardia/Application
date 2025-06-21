import React, { useEffect, useRef, useState, useCallback } from 'react'

export const useEmailProgress = () => {
    const [progress, setProgress] = useState(null)
    const [connected, setConnected] = useState(false)
    const [error, setError] = useState(null)
    const socketRef = useRef(null)
    const reconnectTimeoutRef = useRef(null)
    const isConnectingRef = useRef(false)

    const connect = useCallback(() => {
        if (isConnectingRef.current || (socketRef.current?.readyState === WebSocket.OPEN)) {
            return
        }

        isConnectingRef.current = true
        setError(null)

        try {
            socketRef.current = new WebSocket('ws://localhost:8000/ws/progress/')
            
            socketRef.current.onopen = () => {
                setConnected(true)
                isConnectingRef.current = false
                setError(null)
                console.log("Connected to WebSocket server")
            }

            socketRef.current.onmessage = (event) => {
                try {
                    const progressData = JSON.parse(event.data)
                    setProgress(progressData)
                } catch (parseError) {
                    console.error("Failed to parse progress data:", parseError)
                    setError("Invalid data received")
                }
            }

            socketRef.current.onclose = (event) => {
                setConnected(false)
                isConnectingRef.current = false
                console.log("Disconnected from WebSocket server:", event.code, event.reason)
                
                // Only reconnect if not a clean close (code 1000) and not intentional disconnect
                if (event.code !== 1000 && socketRef.current) {
                    reconnectTimeoutRef.current = setTimeout(() => {
                        connect()
                    }, 3000)
                }
            }

            socketRef.current.onerror = (error) => {
                console.error("WebSocket error:", error)
                setError("Connection error")
                isConnectingRef.current = false
            }

        } catch (connectionError) {
            console.error("Failed to create WebSocket:", connectionError)
            setError("Failed to connect")
            isConnectingRef.current = false
        }
    }, [])

    useEffect(() => {
        connect()

        return () => {
            if (reconnectTimeoutRef.current) {
                clearTimeout(reconnectTimeoutRef.current)
            }
            if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
                socketRef.current.close(1000, "Component unmounting")
            }
            socketRef.current = null
        }
    }, [connect])

    const disconnect = useCallback(() => {
        if (reconnectTimeoutRef.current) {
            clearTimeout(reconnectTimeoutRef.current)
        }
        if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
            socketRef.current.close(1000, "Manual disconnect")
        }
        setConnected(false)
    }, [])

    const reconnect = useCallback(() => {
        disconnect()
        setTimeout(connect, 100)
    }, [connect, disconnect])

    return { progress, connected, error, reconnect, disconnect }
}
