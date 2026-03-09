import React from 'react';
import { cn } from '../lib/utils';

export const Button = React.forwardRef(({ className, variant = 'primary', size = 'default', children, ...props }, ref) => {
    const baseClasses = "inline-flex items-center justify-center whitespace-nowrap font-sans font-semibold uppercase tracking-wider transition-all duration-superfast focus-visible:outline-none focus-visible:ring-[2px] focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:pointer-events-none disabled:opacity-50 relative group rounded-none";

    const variants = {
        primary: "text-accent bg-transparent hover:text-accent",
        outline: "text-foreground border border-foreground bg-transparent hover:bg-foreground hover:text-background",
        ghost: "text-mutedForeground bg-transparent hover:text-foreground border-none"
    };

    const sizes = {
        default: "h-12 gap-2.5 px-6",
        sm: "h-10 gap-2 text-sm px-4",
        lg: "h-14 gap-3 px-8 text-lg",
        none: "h-auto p-0"
    };

    const isPrimary = variant === 'primary';

    return (
        <button
            ref={ref}
            className={cn(
                baseClasses,
                variants[variant],
                // Primary shouldn't have horizontal padding 
                isPrimary ? "px-0 active:translate-y-px py-3" : sizes[size],
                className
            )}
            {...props}
        >
            {/* Ghost Underline animation */}
            {variant === 'ghost' && (
                <span className="absolute bottom-2 left-4 w-[calc(100%-2rem)] h-px bg-foreground origin-left scale-x-0 transition-transform duration-superfast group-hover:scale-x-100" />
            )}

            {/* Primary Underline animation */}
            {isPrimary && (
                <span className="absolute -bottom-1 left-0 w-full h-0.5 bg-accent origin-center scale-x-100 transition-transform duration-superfast group-hover:scale-x-110" />
            )}

            {children}
        </button>
    );
});

Button.displayName = "Button";
