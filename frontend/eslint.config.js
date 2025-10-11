import js from "@eslint/js"
import react from "eslint-plugin-react"
import importPlugin from "eslint-plugin-import"
import globals from "globals"            // 👈 add this

export default [
  js.configs.recommended,
  {
    files: ["**/*.{js,jsx}"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      parserOptions: { ecmaFeatures: { jsx: true } },
      globals: {
        ...globals.browser,              // 👈 tells ESLint about fetch, window, etc.
      },
    },
    plugins: { react, import: importPlugin },
    rules: {
      "import/no-unresolved": "error",
      "react/react-in-jsx-scope": "off",
      "react/prop-types": "off",
      "react/jsx-uses-vars": "error",
    },
    settings: {
      react: { version: "detect" },
      "import/resolver": {
        alias: { map: [["src", "./src"]], extensions: [".js", ".jsx", ".json"] },
        node: { extensions: [".js", ".jsx", ".json"] },
      },
    },
  },
]