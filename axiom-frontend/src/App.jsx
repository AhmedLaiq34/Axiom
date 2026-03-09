import React, { useState } from 'react';
// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion';
import { LandingPage } from './components/LandingPage';
import { ClassCard } from './components/ClassCard';
import { ChatInterface } from './components/ChatInterface';
import { H1, Body } from './components/Typography';
import { useDirectionalReveal } from './lib/utils';

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const { ref: tutorsRef, animate: tutorsAnimate } = useDirectionalReveal("-50px");

  const handleOpenChat = (courseName) => {
    setSelectedCourse(courseName);
    setIsChatOpen(true);
  };

  return (
    <div className="min-h-screen bg-background relative selection:bg-accent selection:text-white">
      <LandingPage />

      {/* Tutors Section */}
      <motion.section
        id="tutors-section"
        ref={tutorsRef}
        initial="hiddenBelow"
        animate={tutorsAnimate}
        variants={{
          hiddenAbove: { opacity: 0, y: -40 },
          hiddenBelow: { opacity: 0, y: 40 },
          visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: [0.25, 0, 0, 1] } }
        }}
        className="py-28 md:py-40 px-6 md:px-16 max-w-5xl mx-auto"
      >
        <div className="mb-16 flex flex-col items-center text-center">
          <H1>Tutors:</H1>
          <Body className="text-mutedForeground mt-4 max-w-2xl text-lg md:text-xl">
            Select a course below to start a live tutoring session with your specialized AI assistant.
          </Body>
        </div>

        <div className="flex justify-center mx-auto w-full max-w-lg">
          <ClassCard
            title="Programming Fundamentals"
            subtitle="Beat Programming Fundamentals at FAST!"
            onClick={() => handleOpenChat("Programming Fundamentals")}
          />
        </div>
      </motion.section>

      {/* Chat Interface */}
      <ChatInterface
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        courseName={selectedCourse || ""}
      />
    </div>
  );
}

export default App;
