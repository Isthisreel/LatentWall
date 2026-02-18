import { motion } from 'framer-motion'

export default function Controls({ isActive, onStart, onStop, connectionStatus, energyLevel }) {
    return (
        <div className="p-6 bg-dino-surface border-t border-dino-primary/20">
            <div className="max-w-4xl mx-auto">
                {/* Main Controls */}
                <div className="flex items-center justify-center gap-4 mb-4">
                    {!isActive ? (
                        <motion.button
                            onClick={onStart}
                            className="btn-cyber px-8 py-4 bg-dino-primary text-dino-background font-cyber font-bold text-lg rounded-lg border-2 border-dino-primary hover:bg-transparent hover:text-dino-primary transition-all relative z-10"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            <span className="relative z-10 flex items-center gap-2">
                                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                                    <path d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" />
                                </svg>
                                START LISTENING
                            </span>
                        </motion.button>
                    ) : (
                        <motion.button
                            onClick={onStop}
                            className="btn-cyber px-8 py-4 bg-dino-secondary text-white font-cyber font-bold text-lg rounded-lg border-2 border-dino-secondary hover:bg-transparent hover:text-dino-secondary transition-all relative z-10"
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                            animate={{
                                boxShadow: [
                                    '0 0 20px rgba(255, 0, 110, 0.4)',
                                    '0 0 40px rgba(255, 0, 110, 0.6)',
                                    '0 0 20px rgba(255, 0, 110, 0.4)',
                                ]
                            }}
                            transition={{ duration: 2, repeat: Infinity }}
                        >
                            <span className="relative z-10 flex items-center gap-2">
                                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clipRule="evenodd" />
                                </svg>
                                STOP
                            </span>
                        </motion.button>
                    )}
                </div>

                {/* Status Bar */}
                <div className="grid grid-cols-3 gap-4">
                    {/* Connection Status */}
                    <div className="p-3 bg-dino-background/50 rounded border border-dino-primary/10 text-center">
                        <div className="text-xs text-dino-text-dim font-mono mb-1">CONNECTION</div>
                        <div className={`text-sm font-cyber ${connectionStatus === 'connected' ? 'text-dino-primary' : 'text-dino-text-dim'}`}>
                            {connectionStatus === 'connected' ? '● ONLINE' : '○ OFFLINE'}
                        </div>
                    </div>

                    {/* Energy Level */}
                    <div className="p-3 bg-dino-background/50 rounded border border-dino-accent/10 text-center">
                        <div className="text-xs text-dino-text-dim font-mono mb-1">ENERGY</div>
                        <div className="text-sm font-cyber text-dino-accent uppercase">
                            {energyLevel || 'SILENT'}
                        </div>
                    </div>

                    {/* Mode */}
                    <div className="p-3 bg-dino-background/50 rounded border border-dino-secondary/10 text-center">
                        <div className="text-xs text-dino-text-dim font-mono mb-1">MODE</div>
                        <div className="text-sm font-cyber text-dino-secondary">
                            {isActive ? 'ACTIVE' : 'STANDBY'}
                        </div>
                    </div>
                </div>

                {/* Info Text */}
                <motion.div
                    className="mt-4 text-center text-xs text-dino-text-dim font-mono"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                >
                    {isActive ? (
                        'Analyzing audio and generating Dino 26 visuals in real-time...'
                    ) : (
                        'Click START LISTENING to begin audio-reactive visual generation'
                    )}
                </motion.div>
            </div>
        </div>
    )
}
