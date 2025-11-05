import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Button } from "@/components/ui/button";

export default function TooltipTestPage() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-8">
      <div className="bg-white rounded-lg shadow-lg p-12">
        <h1 className="text-3xl font-bold mb-8 text-gray-900">Tooltip Test</h1>
        
        <div className="space-y-8">
          {/* Test 1: Simple tooltip */}
          <div>
            <h2 className="text-lg font-semibold mb-4">Test 1: Simple Tooltip</h2>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button>Hover me</Button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>This is a tooltip</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>

          {/* Test 2: Tooltip with icon button */}
          <div>
            <h2 className="text-lg font-semibold mb-4">Test 2: Icon Button</h2>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <button className="px-4 py-2 bg-blue-600 text-white rounded">
                    Click me
                  </button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Another tooltip here</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>

          {/* Test 3: Multiple tooltips */}
          <div>
            <h2 className="text-lg font-semibold mb-4">Test 3: Multiple Tooltips</h2>
            <TooltipProvider>
              <div className="flex gap-4">
                <Tooltip>
                  <TooltipTrigger asChild>
                    <button className="px-3 py-2 bg-green-600 text-white rounded">
                      Green
                    </button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Green button tooltip</p>
                  </TooltipContent>
                </Tooltip>

                <Tooltip>
                  <TooltipTrigger asChild>
                    <button className="px-3 py-2 bg-red-600 text-white rounded">
                      Red
                    </button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Red button tooltip</p>
                  </TooltipContent>
                </Tooltip>

                <Tooltip>
                  <TooltipTrigger asChild>
                    <button className="px-3 py-2 bg-purple-600 text-white rounded">
                      Purple
                    </button>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p>Purple button tooltip</p>
                  </TooltipContent>
                </Tooltip>
              </div>
            </TooltipProvider>
          </div>
        </div>
      </div>
    </div>
  );
}

