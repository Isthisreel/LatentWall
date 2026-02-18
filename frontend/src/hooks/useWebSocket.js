import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'

const WS_URL = 'ws://localhost:8000/ws/stream'

/**
 * Custom hook for WebSocket connection
 */
export function useWebSocket() {
    const [isConnected, setIsConnected] = useState(false)
    const [messages, setMessages] = useState([])
    const [lastMessage, setLastMessage] = useState(null)
    const ws = useRef(null)

    useEffect(() => {
        return () => {
            if (ws.current) {
                ws.current.close()
            }
        }
    }, [])

    const connect = () => {
        if (ws.current?.readyState === WebSocket.OPEN) {
            console.log('Already connected')
            return
        }

        ws.current = new WebSocket(WS_URL)

        ws.current.onopen = () => {
            console.log('✅ WebSocket connected')
            setIsConnected(true)
        }

        ws.current.onmessage = (event) => {
            const data = JSON.parse(event.data)
            console.log('📨 Received:', data)

            setLastMessage(data)
            setMessages(prev => [...prev, data])
        }

        ws.current.onerror = (error) => {
            console.error('❌ WebSocket error:', error)
        }

        ws.current.onclose = () => {
            console.log('🔌 WebSocket disconnected')
            setIsConnected(false)
        }
    }

    const disconnect = () => {
        if (ws.current) {
            ws.current.close()
            ws.current = null
        }
    }

    const sendAudio = (audioBlob) => {
        if (ws.current?.readyState === WebSocket.OPEN) {
            ws.current.send(audioBlob)
        }
    }

    const sendMessage = (message) => {
        if (ws.current?.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify(message))
        }
    }

    return {
        isConnected,
        messages,
        lastMessage,
        connect,
        disconnect,
        sendAudio,
        sendMessage
    }
}
