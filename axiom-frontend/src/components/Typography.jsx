import React from 'react';
import { cn, useDirectionalReveal } from '../lib/utils';
// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion';

const revealVariants = {
    hiddenAbove: { opacity: 0, y: -40 },
    hiddenBelow: { opacity: 0, y: 40 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.25, 0, 0, 1] } }
};

export const HeroText = ({ children, className, ...props }) => {
    const { ref, animate } = useDirectionalReveal("-100px");
    return (
        <motion.h1
            ref={ref}
            initial="hiddenBelow"
            animate={animate}
            variants={revealVariants}
            className={cn("text-5xl md:text-6xl lg:text-8xl font-sans tracking-tighter leading-none font-bold text-foreground", className)}
            {...props}
        >
            {children}
        </motion.h1>
    );
};

export const H1 = ({ children, className, ...props }) => {
    const { ref, animate } = useDirectionalReveal("-50px");
    return (
        <motion.h1
            ref={ref}
            initial="hiddenBelow"
            animate={animate}
            variants={revealVariants}
            className={cn("text-4xl md:text-5xl lg:text-7xl font-sans tracking-tighter leading-tight font-bold text-foreground", className)}
            {...props}
        >
            {children}
        </motion.h1>
    );
};

export const H2 = ({ children, className, ...props }) => {
    const { ref, animate } = useDirectionalReveal("-40px");
    return (
        <motion.h2
            ref={ref}
            initial="hiddenBelow"
            animate={animate}
            variants={{
                ...revealVariants,
                hiddenAbove: { opacity: 0, y: -20 },
                hiddenBelow: { opacity: 0, y: 20 },
                visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.25, 0, 0, 1] } }
            }}
            className={cn("text-3xl md:text-4xl font-sans tracking-tight leading-snug font-bold text-foreground", className)}
            {...props}
        >
            {children}
        </motion.h2>
    );
};

export const Subhead = ({ children, className, ...props }) => (
    <h3 className={cn("text-xl md:text-2xl font-sans tracking-tight leading-snug font-semibold text-foreground", className)} {...props}>
        {children}
    </h3>
);

export const Body = ({ children, className, ...props }) => (
    <p className={cn("text-base md:text-lg font-sans tracking-normal leading-relaxed text-foreground", className)} {...props}>
        {children}
    </p>
);

export const Label = ({ children, className, ...props }) => (
    <span className={cn("font-mono text-xs md:text-sm uppercase tracking-wider text-mutedForeground", className)} {...props}>
        {children}
    </span>
);

export const DisplayText = ({ children, className, ...props }) => (
    <blockquote className={cn("text-2xl md:text-3xl font-display italic text-foreground text-center", className)} {...props}>
        {children}
    </blockquote>
);
