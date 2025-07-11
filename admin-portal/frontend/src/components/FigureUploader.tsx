import React, { useState } from 'react';
import { ProjectFigure } from '../types';

interface FigureUploaderProps {
  projectId: number;
  onUpload: (data: FormData) => Promise<void>;
  existingFigures: ProjectFigure[];
}

export const FigureUploader: React.FC<FigureUploaderProps> = ({ 
  projectId, 
  onUpload, 
  existingFigures 
}) => {
  const [title, setTitle] = useState('');
  const [caption, setCaption] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreviewUrl(URL.createObjectURL(selectedFile));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !title) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('title', title);
    formData.append('caption', caption);
    formData.append('order_index', existingFigures.length.toString());
    formData.append('file', file);

    try {
      await onUpload(formData);
      // Reset form
      setTitle('');
      setCaption('');
      setFile(null);
      setPreviewUrl(null);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="border rounded-lg p-4">
      <h3 className="text-lg font-medium mb-4">Upload Figure</h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Title</label>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Caption</label>
          <textarea
            value={caption}
            onChange={(e) => setCaption(e.target.value)}
            rows={2}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Image File</label>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            required
            className="mt-1 block w-full"
          />
        </div>

        {previewUrl && (
          <div className="mt-4">
            <img 
              src={previewUrl} 
              alt="Preview" 
              className="max-w-full h-48 object-contain"
            />
          </div>
        )}

        <button
          type="submit"
          disabled={uploading || !file || !title}
          className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {uploading ? 'Uploading...' : 'Upload Figure'}
        </button>
      </form>
    </div>
  );
};
