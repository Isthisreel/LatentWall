import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

export default function VideoPlayer({ videoUrl, status, jobId }) {
    const [isLoading, setIsLoading] = useState(false)

    useEffect(() => {
        setIsLoading(status === 'processing')
    }, [status])

    return (
        <div className="h-full flex flex-col p-6 bg-dino-surface border border-dino-secondary/20 rounded-lg">
            {/* Header */}
            <div className="mb-4">
                <h2 className="text-2xl font-cyber font-bold text-dino-secondary mb-2">
                    VISUAL OUTPUT
                </h2>
                <div className="flex items-center gap-2">
                    <div className={`status-dot ${videoUrl ? 'active' : 'inactive'}`}></div>
                    <span className="text-sm text-dino-text-dim font-mono">
                        {isLoading ? 'GENERATING...' : videoUrl ? 'READY' : 'AWAITING INPUT'}
                    </span>
                </div>
            </div>

            {/* Video Container */}
            <div className="flex-1 flex items-center justify-center relative vhs-distortion">
                <AnimatePresence mode="wait">
                    {isLoading && (
                        <motion.div
                            key="loading"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="flex flex-col items-center gap-4"
                        >
                            <div className="spinner"></div>
                            <div className="text-center">
                                <div className="text-dino-accent font-mono text-sm mb-1">
                                    ODYSSEY GENERATION IN PROGRESS
                                </div>
                                <div className="text-dino-text-dim font-mono text-xs">
                                    {jobId && `JOB: ${jobId.substring(0, 8)}...`}
                                </div>
                            </div>

                            {/* Glitch Effect */}
                            <div className="glitch text-4xl font-cyber" data-text="DINO 26">
                                DINO 26
                            </div>
                        </motion.div>
                    )}

                    {!isLoading && videoUrl && (
                        <motion.video
                            key="video"
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            src={videoUrl}
                            controls
                            autoPlay
                            loop
                            className="max-w-full max-h-full rounded-lg"
                        />
                    )}

                    {!isLoading && !videoUrl && (
                        <motion.div
                            key="placeholder"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="text-center"
                        >
                            <div className="text-6xl mb-4">🦖</div>
                            <div className="text-dino-text-dim font-mono text-sm">
                                Start listening to generate visuals
                            </div>
                            <div className="mt-4 text-dino-primary/50 font-mono text-xs">
                                CYBERPUNK PREHISTORIC FUSION
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Corner Accents */}
                <div className="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-dino-secondary/50"></div>
                <div className="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-dino-secondary/50"></div>
                <div className="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-dino-secondary/50"></div>
                <div className="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-dino-secondary/50"></div>
            </div>

            {/* Metadata */}
            {videoUrl && (
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-4 p-3 bg-dino-background/50 rounded border border-dino-secondary/20"
                >
                    <div className="flex items-center justify-between">
                        <span className="text-xs text-dino-text-dim font-mono">ODYSSEY URL</span>
                        <a
                            href={videoUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-xs text-dino-secondary hover:text-dino-accent font-mono underline"
                        >
                            OPEN IN NEW TAB →
                        </a>
                    </div>
                </motion.div>
            )}
        </div>
    )
}
