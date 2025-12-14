import { Link } from "react-router-dom";
import { CheckCircle, Home, User, Mail, ArrowRight } from "lucide-react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";

export default function ApplicationThankYouPage() {
  const isNewUser = localStorage.getItem("is_new_user") === "true";

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white flex items-center justify-center p-4">
      <div className="max-w-lg w-full">
        <Card className="border-green-200">
          <CardHeader className="text-center pb-2">
            <div className="mx-auto mb-4 h-20 w-20 bg-green-100 rounded-full flex items-center justify-center">
              <CheckCircle className="h-12 w-12 text-green-600" />
            </div>
            <CardTitle className="text-2xl text-green-800">
              ¡Candidatura Enviada!
            </CardTitle>
            <CardDescription className="text-base">
              Tu candidatura ha sido recibida correctamente
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-6">
            {/* Confirmation message */}
            <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
              <Mail className="h-8 w-8 text-green-600 mx-auto mb-2" />
              <p className="text-green-800">
                Te hemos enviado un correo de confirmación con los detalles de tu candidatura.
              </p>
            </div>

            {/* What's next */}
            <div className="space-y-3">
              <h3 className="font-semibold text-gray-900">¿Qué sigue?</h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-start gap-2">
                  <ArrowRight className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                  <span>El equipo de selección revisará tu perfil</span>
                </li>
                <li className="flex items-start gap-2">
                  <ArrowRight className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                  <span>Te contactarán si tu perfil encaja con la posición</span>
                </li>
                <li className="flex items-start gap-2">
                  <ArrowRight className="h-4 w-4 text-blue-500 mt-0.5 flex-shrink-0" />
                  <span>Puedes seguir el estado de tu candidatura desde tu perfil</span>
                </li>
              </ul>
            </div>

            {/* Password setup notice for new users */}
            {isNewUser && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <h4 className="font-medium text-yellow-900 mb-1">
                  Establece tu contraseña
                </h4>
                <p className="text-sm text-yellow-800">
                  Te hemos enviado un correo para que configures tu contraseña.
                  Con ella podrás acceder a tu perfil y gestionar tus candidaturas.
                </p>
              </div>
            )}

            {/* Action buttons */}
            <div className="flex flex-col gap-3 pt-2">
              <Link to="/candidate/profile">
                <Button className="w-full" size="lg">
                  <User className="h-4 w-4 mr-2" />
                  Ver mi perfil
                </Button>
              </Link>
              <Link to="/">
                <Button variant="outline" className="w-full">
                  <Home className="h-4 w-4 mr-2" />
                  Volver al inicio
                </Button>
              </Link>
            </div>

            {/* Footer note */}
            <p className="text-xs text-gray-500 text-center">
              Si tienes alguna pregunta sobre el proceso de selección,
              contacta directamente con la empresa.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
