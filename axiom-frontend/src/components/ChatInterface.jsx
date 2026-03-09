import React, { useState, useRef, useEffect } from 'react';
import { X, Send, Loader2 } from 'lucide-react';
import { Label } from './Typography';
import { cn } from '../lib/utils';
// eslint-disable-next-line no-unused-vars
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export const ChatInterface = ({ isOpen, onClose, courseName }) => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        if (courseName && (messages.length === 0 || messages.length === 1)) {
            setMessages([
                { role: 'assistant', text: `Hello! I'm your tutor for ${courseName}. How can I help you today?` }
            ]);
        }
    }, [courseName]);

    useEffect(() => {
        if (isOpen) {
            scrollToBottom();
        }
    }, [messages, isOpen]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', text: userMessage }]);
        setIsLoading(true);

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: userMessage })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to get response');
            }

            setMessages(prev => [...prev, {
                role: 'assistant',
                text: data.response,
                sources: data.sources
            }]);
        } catch (error) {
            setMessages(prev => [...prev, {
                role: 'system',
                text: `Error: ${error.message}. Please try again.`
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <motion.div
                    initial={{ opacity: 0, scale: 0.95, y: 20 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.95, y: 20 }}
                    transition={{ duration: 0.2, ease: [0.25, 0, 0, 1] }}
                    className="fixed inset-0 md:inset-auto md:bottom-8 md:left-1/2 md:-translate-x-1/2 w-full md:w-[600px] lg:w-[700px] h-[100dvh] md:h-[650px] z-50 bg-background md:border md:border-border flex flex-col md:shadow-2xl"
                >
                    {/* Header */}
                    <div className="border-b border-border p-4 flex justify-between items-center bg-muted/50">
                        <div>
                            <Label className="text-accent mb-1 inline-block">Live Tutor</Label>
                            <h3 className="text-lg font-sans font-bold tracking-tight text-foreground">{courseName}</h3>
                        </div>
                        <button
                            onClick={onClose}
                            className="text-mutedForeground hover:text-foreground transition-colors p-2 focus:outline-none focus:ring-2 focus:ring-accent"
                        >
                            <X strokeWidth={1.5} className="w-5 h-5" />
                        </button>
                    </div>

                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-6">
                        {messages.map((msg, i) => (
                            <div key={i} className={cn("flex flex-col", msg.role === 'user' ? "items-end" : "items-start")}>
                                <div
                                    className={cn(
                                        "max-w-[85%] p-4 text-sm md:text-base leading-relaxed font-sans prose prose-invert w-full overflow-hidden whitespace-normal break-words",
                                        msg.role === 'user'
                                            ? "bg-foreground text-background prose-p:text-background prose-headings:text-background prose-strong:text-background"
                                            : msg.role === 'system'
                                                ? "bg-red-950/30 text-red-500 border border-red-900/50"
                                                : "bg-muted text-foreground border border-border"
                                    )}
                                >
                                    <ReactMarkdown
                                        remarkPlugins={[remarkGfm]}
                                        components={{
                                            // eslint-disable-next-line no-unused-vars
                                            p: ({ node, ...props }) => <p className="mb-4 last:mb-0 leading-relaxed" {...props} />,
                                            // eslint-disable-next-line no-unused-vars
                                            h1: ({ node, ...props }) => <h1 className="text-2xl font-bold mb-4 mt-6 first:mt-0" {...props} />,
                                            // eslint-disable-next-line no-unused-vars
                                            h2: ({ node, ...props }) => <h2 className="text-xl font-bold mb-3 mt-5 first:mt-0" {...props} />,
                                            // eslint-disable-next-line no-unused-vars
                                            h3: ({ node, ...props }) => <h3 className="text-lg font-bold mb-2 mt-4 first:mt-0" {...props} />,
                                            // eslint-disable-next-line no-unused-vars
                                            ul: ({ node, ...props }) => <ul className="list-disc pl-6 mb-4 space-y-1" {...props} />,
                                            // eslint-disable-next-line no-unused-vars
                                            ol: ({ node, ...props }) => <ol className="list-decimal pl-6 mb-4 space-y-1" {...props} />,
                                            // eslint-disable-next-line no-unused-vars
                                            li: ({ node, ...props }) => <li className="mb-1" {...props} />,
                                            // eslint-disable-next-line no-unused-vars
                                            a: ({ node, ...props }) => <a className="text-accent underline hover:text-white break-all" target="_blank" rel="noopener noreferrer" {...props} />,
                                            // eslint-disable-next-line no-unused-vars
                                            code: ({ node, inline, ...props }) =>
                                                inline
                                                    ? <code className="bg-background px-1.5 py-0.5 text-sm font-mono text-[#FF3D00] break-words whitespace-pre-wrap" {...props} />
                                                    : <div className="overflow-x-auto bg-background mb-4 border border-border w-full"><code className="block p-4 text-sm font-mono text-left whitespace-pre" {...props} /></div>,
                                            // eslint-disable-next-line no-unused-vars
                                            blockquote: ({ node, ...props }) => <blockquote className="border-l-2 border-accent pl-4 italic opacity-80 mb-4" {...props} />,
                                        }}
                                    >
                                        {msg.text}
                                    </ReactMarkdown>
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="flex items-start">
                                <div className="bg-muted text-foreground border border-border p-4 flex items-center gap-3">
                                    <Loader2 className="w-4 h-4 animate-spin text-accent" />
                                    <span className="text-sm">Thinking...</span>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input */}
                    <div className="p-4 border-t border-border bg-background">
                        <form onSubmit={handleSubmit} className="relative flex items-center">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder="Ask about your course..."
                                className="w-full bg-input border border-border text-foreground placeholder:text-mutedForeground h-14 px-4 pr-12 focus:outline-none focus:border-accent transition-colors font-sans"
                            />
                            <button
                                type="submit"
                                disabled={isLoading || !input.trim()}
                                className="absolute right-2 top-2 bottom-2 w-10 flex items-center justify-center text-accent hover:text-foreground disabled:opacity-50 transition-colors focus:outline-none focus:ring-2 focus:ring-inset focus:ring-accent"
                            >
                                <Send className="w-5 h-5" strokeWidth={1.5} />
                            </button>
                        </form>
                    </div>
                </motion.div>
            )}
        </AnimatePresence >
    );
};
