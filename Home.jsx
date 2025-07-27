import React from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import heroImage from "../assets/hero.jpg";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white">
      <header className="p-6 flex justify-between items-center border-b border-gray-700">
        <h1 className="text-3xl font-bold text-cyan-400">AITO</h1>
        <nav className="space-x-4">
          <button
            className="hover:text-cyan-400 transition"
            onClick={() => navigate("/")}
          >
            Home
          </button>
          <button
            className="hover:text-cyan-400 transition"
            onClick={() => navigate("/form")}
          >
            Smart Routing
          </button>
        </nav>
      </header>

      <main className="flex flex-col-reverse lg:flex-row items-center justify-between p-10 lg:p-20">
        <motion.div
          className="text-center lg:text-left max-w-xl"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
        >
          <h2 className="text-4xl lg:text-6xl font-bold leading-tight mb-4">
            AI-Powered <span className="text-cyan-400">Traffic Optimization</span>
          </h2>
          <p className="text-lg text-gray-300 mb-6">
            Empowering public transport with smart routing decisions based on real-time city context, human activity, and traffic data.
          </p>
          <button
            onClick={() => navigate("/form")}
            className="px-6 py-3 bg-cyan-500 hover:bg-cyan-600 text-white font-semibold rounded-lg shadow-lg transition"
          >
            Get Started
          </button>
        </motion.div>

        <motion.img
          src={heroImage}
          alt="AI Traffic"
          className="w-full max-w-lg rounded-lg shadow-2xl mb-10 lg:mb-0"
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 1 }}
        />
      </main>

      <section className="px-6 py-20 bg-gray-900">
        <h3 className="text-2xl font-bold text-cyan-400 mb-6 text-center">
          What makes AITO different?
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
          {[
            {
              title: "Human-Centric AI",
              desc: "Considers human factors like weather, school schedules, events."
            },
            {
              title: "Real-time Insights",
              desc: "Uses live traffic patterns and predictions for better routing."
            },
            {
              title: "Built for Public Transport",
              desc: "Designed to work within the limits of fixed bus routes."
            }
          ].map((item, idx) => (
            <motion.div
              key={idx}
              className="bg-gray-800 p-6 rounded-xl shadow-xl hover:shadow-cyan-500/20 transition"
              whileHover={{ scale: 1.03 }}
            >
              <h4 className="text-xl font-semibold text-cyan-300 mb-2">
                {item.title}
              </h4>
              <p className="text-gray-400 text-sm">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      <footer className="text-center py-6 text-sm text-gray-500">
        &copy; {new Date().getFullYear()} AITO. All rights reserved.
      </footer>
    </div>
  );
};

export default Home;
