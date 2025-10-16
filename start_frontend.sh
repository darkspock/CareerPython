#!/bin/bash

echo "🚀 Iniciando servidor de desarrollo frontend..."
echo "📍 Navegando a client-vite..."

cd client-vite

echo "📦 Instalando dependencias..."
npm install

echo "🔥 Iniciando servidor de desarrollo..."
echo "🌐 El frontend estará disponible en: http://localhost:5173"
echo "🔗 Backend API disponible en: http://localhost:8000"
echo ""
echo "Páginas disponibles:"
echo "  - Landing: http://localhost:5173/"
echo "  - Login: http://localhost:5173/auth/login"
echo "  - Registro: http://localhost:5173/auth/register"
echo "  - Dashboard: http://localhost:5173/dashboard"
echo ""

npm run dev