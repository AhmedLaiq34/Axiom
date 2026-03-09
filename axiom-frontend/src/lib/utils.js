import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { useRef, useState, useEffect } from 'react';
import { useInView } from 'framer-motion';

export function cn(...inputs) {
    return twMerge(clsx(inputs));
}

export function useDirectionalReveal(margin = "-50px") {
    const ref = useRef(null);
    const isInView = useInView(ref, { margin });
    const [position, setPosition] = useState("below");

    useEffect(() => {
        if (!isInView && ref.current) {
            const rect = ref.current.getBoundingClientRect();
            if (rect.top < window.innerHeight / 2) {
                // eslint-disable-next-line
                setPosition("above");
            } else {
                // eslint-disable-next-line
                setPosition("below");
            }
        }
    }, [isInView]);

    return {
        ref,
        animate: isInView ? "visible" : (position === "above" ? "hiddenAbove" : "hiddenBelow")
    };
}
