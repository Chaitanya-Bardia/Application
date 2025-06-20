import React, { useEffect, useRef, useState } from 'react'

export const useEmailProgress = () => {
    const [progress, setProgress] = useState(null)
    const [connected,setConnected] = useState(false)
    const socketRef = useRef(null)

    useEffect(()=>{
        socketRef.current = new WebSocket('ws://localhost:8000/ws/progress')
        socketRef.current.onopen = () =>{
            setConnected(true);
            console.log("Connected to WebSocket server");
        }
        socketRef.current.onmessage = (event) => {
            const progressData = JSON.parse(event.data);
            setProgress(progressData);
        };

        socketRef.current.onclose = () => {
            setConnected(false);
            console.log("Disconnected from WebSocket server");
        };

        return () => {
            socketRef.current.close();
        };
    },[])

   return {progress,connected}
}
