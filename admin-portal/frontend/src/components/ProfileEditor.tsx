import React, { useState } from 'react';
import { User } from '../types';

interface ProfileEditorProps {
  user: User;
  onUpdate: (data: FormData) => Promise<void>;
}

export const ProfileEditor: React.FC<ProfileEditorProps> = ({ user, onUpdate }) => {
  const [formData, setFormData] = useState({
    about: user.about || '',
    disciplines: user.disciplines?.join(', ') || '',
    research_interests: user.research_interests || '',
    office_location: user.office_location || '',
    office_hours: user.office_hours || '',
    is_profile_public: user.is_profile_public ?? true
  });
  const [profilePicture, setProfilePicture] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setProfilePicture(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const data = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
      if (key === 'disciplines') {
        data.append(key, JSON.stringify(value.split(',').map(d => d.trim()).filter(Boolean)));
      } else {
        data.append(key, value.toString());
      }
    });
    
    if (profilePicture) {
      data.append('profile_picture', profilePicture);
    }
    
    await onUpdate(data);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700">Profile Picture</label>
        <div className="mt-2 flex items-center space-x-4">
          <div className="w-24 h-24 rounded-full overflow-hidden bg-gray-200">
            {previewUrl || user.profile_url ? (
              <img 
                src={previewUrl || user.profile_url} 
                alt="Profile" 
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                No image
              </div>
            )}
          </div>
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            className="text-sm"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">About</label>
        <textarea
          value={formData.about}
          onChange={(e) => setFormData({...formData, about: e.target.value})}
          rows={4}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          placeholder="Tell us about yourself..."
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Disciplines</label>
        <input
          type="text"
          value={formData.disciplines}
          onChange={(e) => setFormData({...formData, disciplines: e.target.value})}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          placeholder="e.g., Public Health, Epidemiology, Biostatistics"
        />
        <p className="mt-1 text-sm text-gray-500">Separate multiple disciplines with commas</p>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Research Interests</label>
        <textarea
          value={formData.research_interests}
          onChange={(e) => setFormData({...formData, research_interests: e.target.value})}
          rows={3}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Office Location</label>
          <input
            type="text"
            value={formData.office_location}
            onChange={(e) => setFormData({...formData, office_location: e.target.value})}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Office Hours</label>
          <input
            type="text"
            value={formData.office_hours}
            onChange={(e) => setFormData({...formData, office_hours: e.target.value})}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
          />
        </div>
      </div>

      <div className="flex items-center">
        <input
          type="checkbox"
          checked={formData.is_profile_public}
          onChange={(e) => setFormData({...formData, is_profile_public: e.target.checked})}
          className="h-4 w-4 text-blue-600 rounded"
        />
        <label className="ml-2 text-sm text-gray-700">
          Make my profile public
        </label>
      </div>

      <button
        type="submit"
        className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700"
      >
        Update Profile
      </button>
    </form>
  );
};
