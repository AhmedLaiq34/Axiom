import React from 'react';
import { cn } from '../lib/utils';
import { H2, Body, Label } from './Typography';
import { ChevronRight } from 'lucide-react';

export const ClassCard = ({ title, subtitle, onClick, className }) => {
    return (
        <div
            onClick={onClick}
            className={cn(
                "group relative border border-border bg-transparent p-6 md:p-8 cursor-pointer transition-colors duration-fast hover:border-hover hover:bg-muted/30 w-full flex flex-col justify-between overflow-hidden",
                className
            )}
        >
            {/* Accent top border dimension effect */}
            <div className="absolute top-0 left-0 h-1 w-16 bg-accent transition-all duration-normal group-hover:w-full" />

            <div className="flex justify-between items-start mb-12">
                <Label className="text-accent">PF CS-1002</Label>
                <ChevronRight strokeWidth={1.5} className="w-6 h-6 text-mutedForeground group-hover:text-foreground transition-colors group-hover:translate-x-1 duration-fast" />
            </div>

            <div className="space-y-3 relative z-10 w-full">
                <H2 className="text-layer-depth text-white" data-text={title}>{title}</H2>
                <Body className="text-mutedForeground max-w-lg">{subtitle}</Body>
            </div>
        </div>
    );
};
