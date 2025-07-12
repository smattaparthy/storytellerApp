/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}", // Scan Vue and JS/TS files for Tailwind classes
  ],
  theme: {
    extend: {
      colors: {
        // Example: Child-friendly purple-to-pink gradients
        // These can be used in classes like bg-gradient-to-r from-primary-purple to-primary-pink
        'primary-purple': '#A770EF', // A nice purple
        'primary-pink': '#F777AA',   // A friendly pink
        'secondary-blue': '#70A7EF',
        'accent-yellow': '#F7D077',
      },
      fontFamily: {
        // Add child-friendly fonts if desired, e.g., 'Comic Sans MS', 'Arial Rounded MT Bold'
        // sans: ['ui-sans-serif', 'system-ui', ...defaultTheme.fontFamily.sans],
        // display: ['YourChildFriendlyFont', 'sans-serif'], // Example
      },
      // Add any other theme customizations here
      // E.g., for smooth animations
      transitionProperty: {
        'height': 'height',
        'spacing': 'margin, padding',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-in': 'slideIn 0.5s ease-out forwards',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
        slideIn: {
          '0%': { transform: 'translateY(20px)', opacity: 0 },
          '100%': { transform: 'translateY(0px)', opacity: 1 },
        }
      }
    },
  },
  plugins: [],
}
