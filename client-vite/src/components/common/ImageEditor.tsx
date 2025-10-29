import React, { useState, useCallback } from 'react'
import Cropper from 'react-easy-crop'

// Define Area type manually since it's not exported in v5
type Area = {
  x: number
  y: number
  width: number
  height: number
}

interface ImageEditorProps {
  src: string
  onCropComplete: (croppedImage: string) => void
  onCancel: () => void
  aspectRatio?: number
  title?: string
}

export const ImageEditor: React.FC<ImageEditorProps> = ({
  src,
  onCropComplete,
  onCancel,
  aspectRatio = 1,
  title = "Editar Imagen"
}) => {
  const [crop, setCrop] = useState({ x: 0, y: 0 })
  const [zoom, setZoom] = useState(1)
  const [croppedAreaPixels, setCroppedAreaPixels] = useState<Area | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)

  const onCropChange = useCallback((crop: any) => {
    setCrop(crop)
  }, [])

  const onZoomChange = useCallback((zoom: number) => {
    setZoom(zoom)
  }, [])

  const onCropCompleteCallback = useCallback((croppedArea: Area, croppedAreaPixels: Area) => {
    setCroppedAreaPixels(croppedAreaPixels)
  }, [])

  const createCroppedImage = useCallback(async () => {
    if (!croppedAreaPixels) return

    setIsProcessing(true)
    try {
      const croppedImage = await getCroppedImg(src, croppedAreaPixels)
      onCropComplete(croppedImage)
    } catch (err) {
      console.error('Error cropping image:', err)
    } finally {
      setIsProcessing(false)
    }
  }, [croppedAreaPixels, src, onCropComplete])

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-hidden">
        <h3 className="text-lg font-semibold mb-4">{title}</h3>
        
        <div className="relative w-full h-96 mb-4 bg-gray-100 rounded-lg overflow-hidden">
          <Cropper
            image={src}
            crop={crop}
            zoom={zoom}
            aspect={aspectRatio}
            onCropChange={onCropChange}
            onZoomChange={onZoomChange}
            onCropComplete={onCropCompleteCallback}
            showGrid={true}
            style={{
              containerStyle: {
                borderRadius: '8px'
              }
            }}
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-2 text-gray-700">
            Zoom: {Math.round(zoom * 100)}%
          </label>
          <input
            type="range"
            min={1}
            max={3}
            step={0.1}
            value={zoom}
            onChange={(e) => setZoom(Number(e.target.value))}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
          />
        </div>

        <div className="flex gap-2 justify-end">
          <button
            onClick={onCancel}
            disabled={isProcessing}
            className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Cancelar
          </button>
          <button
            onClick={createCroppedImage}
            disabled={isProcessing || !croppedAreaPixels}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            {isProcessing ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                Procesando...
              </>
            ) : (
              'Aplicar'
            )}
          </button>
        </div>
      </div>
    </div>
  )
}

// Función helper para crear la imagen recortada
const getCroppedImg = (imageSrc: string, pixelCrop: Area): Promise<string> => {
  return new Promise((resolve, reject) => {
    const image = new Image()
    image.crossOrigin = 'anonymous'
    image.src = imageSrc
    image.onload = () => {
      try {
        const canvas = document.createElement('canvas')
        const ctx = canvas.getContext('2d')
        
        if (!ctx) {
          reject(new Error('No se pudo obtener el contexto del canvas'))
          return
        }

        canvas.width = pixelCrop.width
        canvas.height = pixelCrop.height

        ctx.drawImage(
          image,
          pixelCrop.x,
          pixelCrop.y,
          pixelCrop.width,
          pixelCrop.height,
          0,
          0,
          pixelCrop.width,
          pixelCrop.height
        )

        // Convertir a JPEG con calidad del 90%
        resolve(canvas.toDataURL('image/jpeg', 0.9))
      } catch (error) {
        reject(error)
      }
    }
    image.onerror = () => {
      reject(new Error('Error al cargar la imagen'))
    }
  })
}

export default ImageEditor
