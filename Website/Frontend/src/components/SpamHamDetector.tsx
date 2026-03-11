import { useState } from 'react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import {Upload, Shield, AlertTriangle, CheckCircle, XCircle, FileText, Mail} from 'lucide-react';

interface ScanResult {
  threat: 'safe' | 'suspicious' | 'dangerous';
  detections: {
    type: string;
    severity: 'low' | 'medium' | 'high';
    description: string;
  }[];
}

export function SpamHamDetector() {
  const [scanType, setScanType] = useState<'email' | 'file'>('email');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ScanResult | null>(null);

  const performScan = () => {
    setLoading(true);
    setResult(null);

    setTimeout(() => {
      const mockDetections = [
        {
          type: 'Phishing Attempt',
          severity: 'high' as const,
          description:
            'Email contains suspicious links requesting personal information'
        },
        {
          type: 'Suspicious Sender',
          severity: 'medium' as const,
          description:
            'Sender domain does not match claimed organization'
        },
        {
          type: 'Malicious Attachment',
          severity: 'high' as const,
          description:
            'Attachment contains potentially harmful executable code'
        },
        {
          type: 'Spam Indicators',
          severity: 'low' as const,
          description:
            'Message contains common spam keywords'
        }
      ];

      const isSafe = Math.random() > 0.5;

      const selectedDetections = isSafe
        ? []
        : mockDetections.slice(0, Math.floor(Math.random() * 3) + 1);

      const mockResult: ScanResult = {
        threat: isSafe
          ? 'safe'
          : selectedDetections.some((d) => d.severity === 'high')
          ? 'dangerous'
          : 'suspicious',
        detections: selectedDetections
      };

      setResult(mockResult);
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="space-y-8">

      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-purple-600 to-pink-600 p-8 text-white">
        <div className="relative z-10 grid md:grid-cols-2 gap-8 items-center">
          <div>
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Spam and Ham Detection
            </h2>

            <p className="text-purple-100 text-lg">
              Protect yourself from spam emails and dangerous
              attachments. Our scanning technology identifies threats before
              they can harm you.
            </p>
          </div>

          <div className="hidden md:block">
            <ImageWithFallback
              src="https://images.unsplash.com/photo-1768224656445-33d078c250b7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=1080"
              alt="Cybersecurity"
              className="w-full h-48 object-cover rounded-lg"
            />
          </div>
        </div>
      </div>

      {/* SCAN TYPE */}

      <div className="bg-white rounded-xl shadow-lg p-6 md:p-8">

        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Select Scan Type
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">

          {/* EMAIL */}

          <button
            onClick={() => setScanType('email')}
            className={`p-4 rounded-lg border-2 transition-all ${
              scanType === 'email'
                ? 'border-purple-600 bg-purple-50'
                : 'border-gray-200 hover:border-purple-300'
            }`}
          >
            <Mail
              className={`w-8 h-8 mx-auto mb-2 ${
                scanType === 'email'
                  ? 'text-purple-600'
                  : 'text-gray-400'
              }`}
            />

            <div className="font-medium text-gray-900">
              Email Content
            </div>

            <div className="text-sm text-gray-600 mt-1">
              Scan email text
            </div>
          </button>

          {/* FILE */}

          <button
            onClick={() => setScanType('file')}
            className={`p-4 rounded-lg border-2 transition-all ${
              scanType === 'file'
                ? 'border-purple-600 bg-purple-50'
                : 'border-gray-200 hover:border-purple-300'
            }`}
          >
            <FileText
              className={`w-8 h-8 mx-auto mb-2 ${
                scanType === 'file'
                  ? 'text-purple-600'
                  : 'text-gray-400'
              }`}
            />

            <div className="font-medium text-gray-900">
              File Upload
            </div>

            <div className="text-sm text-gray-600 mt-1">
              Scan attachments
            </div>
          </button>
        </div>

        {/* INPUT AREA */}

        <div className="space-y-4">

          {scanType === 'email' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Paste Email Content
              </label>

              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Paste the email content here to scan for spam or phishing..."
                rows={8}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none"
              />
            </div>
          )}

          {scanType === 'file' && (
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-purple-400 transition-colors">

              <Upload className="w-12 h-12 text-gray-400 mx-auto mb-3" />

              <p className="text-gray-700 font-medium mb-1">
                Drop file here or click to upload
              </p>

              <p className="text-sm text-gray-500">
                Supports: .exe, .zip, .pdf, .doc, .xls
              </p>

              <input
                type="file"
                onChange={(e) =>
                  setContent(e.target.files?.[0]?.name || '')
                }
                className="hidden"
                id="file-upload"
              />

              <label
                htmlFor="file-upload"
                className="inline-block mt-4 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 cursor-pointer"
              >
                Select File
              </label>

              {content && (
                <p className="mt-3 text-sm text-gray-700">
                  Selected: {content}
                </p>
              )}
            </div>
          )}

          {/* SCAN BUTTON */}

          <button
            onClick={performScan}
            disabled={!content || loading}
            className="w-full px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center justify-center gap-2 font-medium"
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Scanning...
              </>
            ) : (
              <>
                <Shield className="w-5 h-5" />
                Scan Now
              </>
            )}
          </button>
        </div>
      </div>

      {/* RESULT */}

      {result && (
        <div className="bg-white rounded-xl shadow-lg p-6 md:p-8 space-y-6">

          <div
            className={`flex items-start gap-4 p-6 rounded-lg border-2 ${
              result.threat === 'safe'
                ? 'bg-green-50 border-green-200'
                : result.threat === 'suspicious'
                ? 'bg-yellow-50 border-yellow-200'
                : 'bg-red-50 border-red-200'
            }`}
          >

            <div className="flex-shrink-0">
              {result.threat === 'safe' && (
                <CheckCircle className="w-12 h-12 text-green-500" />
              )}

              {result.threat === 'suspicious' && (
                <AlertTriangle className="w-12 h-12 text-yellow-500" />
              )}

              {result.threat === 'dangerous' && (
                <XCircle className="w-12 h-12 text-red-500" />
              )}
            </div>

            <div>

              <h3 className="text-2xl font-bold mb-2">

                {result.threat === 'safe' &&
                  'No Threats Detected'}

                {result.threat === 'suspicious' &&
                  'Suspicious Content'}

                {result.threat === 'dangerous' &&
                  'Dangerous Threat Detected'}
              </h3>

              <p className="text-gray-700">

                {result.threat === 'safe' &&
                  'This content appears safe.'}

                {result.threat === 'suspicious' &&
                  'This content shows suspicious patterns.'}

                {result.threat === 'dangerous' &&
                  'This content contains dangerous elements.'}
              </p>
            </div>
          </div>

          {result.detections.length > 0 && (
            <div>

              <h4 className="text-lg font-semibold mb-4">
                Detected Threats ({result.detections.length})
              </h4>

              <div className="space-y-3">

                {result.detections.map((d, i) => (
                  <div
                    key={i}
                    className={`p-4 rounded-lg border-2 ${
                      d.severity === 'high'
                        ? 'border-red-200 bg-red-50'
                        : d.severity === 'medium'
                        ? 'border-yellow-200 bg-yellow-50'
                        : 'border-blue-200 bg-blue-50'
                    }`}
                  >

                    <h5 className="font-medium text-gray-900">
                      {d.type}
                    </h5>

                    <p className="text-sm text-gray-700">
                      {d.description}
                    </p>

                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}