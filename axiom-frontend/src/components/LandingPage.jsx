import React from 'react';
// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion';
import { HeroText, Body, Label } from './Typography';
import { Button } from './Button';
import { ArrowDown } from 'lucide-react';
import { useDirectionalReveal } from '../lib/utils';

export const LandingPage = () => {
    const { ref: logoRef, animate: logoAnimate } = useDirectionalReveal("-50px");

    const containerVariants = {
        hidden: { opacity: 0 },
        show: {
            opacity: 1,
            transition: {
                staggerChildren: 0.15,
                delayChildren: 0.2
            }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 30 },
        show: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.25, 0, 0, 1] } }
    };

    return (
        <div className="min-h-[100dvh] flex flex-col justify-center items-center py-20 px-6 md:px-12 lg:px-16 w-full mx-auto border-b border-border overflow-hidden">
            <motion.div
                variants={containerVariants}
                initial="hidden"
                animate="show"
                className="w-full max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-x-8 lg:gap-x-16 gap-y-4 md:gap-y-6 items-center"
            >
                {/* Label (Row 1 on Desktop) */}
                <motion.div variants={itemVariants} className="col-span-1 md:col-start-6 md:col-span-7 md:row-start-1 flex flex-col items-center md:items-start text-center md:text-left order-2 md:order-1">
                    <Label className="text-accent inline-block text-base md:text-lg lg:text-xl mb-1 mt-4 md:mt-0">Welcome to Axiom</Label>
                    <span className="text-mutedForeground/80 font-mono text-xs md:text-sm tracking-widest uppercase mb-0">The future of learning</span>
                </motion.div>

                {/* Logo (Row 2 Left on Desktop) */}
                <motion.div
                    ref={logoRef}
                    initial="hiddenBelow"
                    animate={logoAnimate}
                    variants={{
                        hiddenAbove: { opacity: 0, y: -40 },
                        hiddenBelow: { opacity: 0, y: 40 },
                        visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.25, 0, 0, 1], delay: 0.2 } }
                    }}
                    className="col-span-1 md:col-start-1 md:col-span-5 md:row-start-2 flex justify-center md:justify-end items-center order-1 md:order-2"
                >
                    <img src="/logo.png" alt="Axiom Logo" className="w-[85%] sm:w-[70%] md:w-[110%] lg:w-[125%] max-w-[650px] h-auto object-contain drop-shadow-2xl md:-mr-4 lg:-mr-12" />
                </motion.div>

                {/* Title (Row 2 Right on Desktop) */}
                <motion.div variants={itemVariants} className="col-span-1 md:col-start-6 md:col-span-7 md:row-start-2 flex flex-col items-center md:items-start text-center md:text-left order-3">
                    <HeroText className="text-5xl sm:text-6xl md:text-6xl lg:text-[7.5rem] leading-[0.9]">
                        Master Your <br />
                        <span className="text-mutedForeground">Coursework</span>
                    </HeroText>
                </motion.div>

                {/* Body & Button (Row 3 Right on Desktop) */}
                <motion.div variants={itemVariants} className="col-span-1 md:col-start-6 md:col-span-7 md:row-start-3 flex flex-col items-center md:items-start text-center md:text-left order-4 mt-2 md:mt-4">
                    <Body className="text-mutedForeground text-lg md:text-xl lg:text-2xl px-4 md:px-0 max-w-2xl">
                        Axiom provides AI tutors tailored to FAST University's curriculum. Experience personalized, instant guidance designed to help you excel.
                    </Body>
                    <div className="pt-8 md:pt-12">
                        <Button variant="primary" className="gap-2 text-base md:text-lg px-8 py-6" onClick={() => {
                            document.getElementById('tutors-section')?.scrollIntoView({ behavior: 'smooth' });
                        }}>
                            <span>Explore Tutors</span>
                            <ArrowDown className="w-5 h-5 pointer-events-none ml-2" strokeWidth={1.5} />
                        </Button>
                    </div>
                </motion.div>
            </motion.div>
        </div>
    );
};
