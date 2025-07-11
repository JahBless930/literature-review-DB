import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import Layout from '../components/Layout';
import { apiService as api } from '../services/api';
import { UserProfile, ProjectSummary } from '../types';

export const SupervisorProfilePage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [projects, setProjects] = useState<ProjectSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfile();
  }, [slug]);

  const fetchProfile = async () => {
    try {
      const response = await api.get(`/supervisors/profile/${slug}`);
      setProfile(response.data.profile);
      setProjects(response.data.projects);
    } catch (error) {
      console.error('Error fetching profile:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Layout><div>Loading...</div></Layout>;
  if (!profile) return <Layout><div>Profile not found</div></Layout>;

  return (
    <Layout>
      <div className="max-w-4xl mx-auto py-8">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-start space-x-6">
            {profile.profile_picture_url && (
              <img 
                src={profile.profile_picture_url} 
                alt={profile.full_name}
                                className="w-32 h-32 rounded-full object-cover"
              />
            )}
            <div className="flex-1">
              <h1 className="text-3xl font-bold">{profile.full_name}</h1>
              <p className="text-gray-600">{profile.institution}</p>
              {profile.department && (
                <p className="text-gray-600">{profile.department}</p>
              )}
              <p className="text-gray-600">{profile.email}</p>
            </div>
          </div>

          {profile.about && (
            <div className="mt-6">
              <h2 className="text-xl font-semibold mb-2">About</h2>
              <p className="text-gray-700 whitespace-pre-wrap">{profile.about}</p>
            </div>
          )}

          {profile.disciplines && profile.disciplines.length > 0 && (
            <div className="mt-6">
              <h2 className="text-xl font-semibold mb-2">Disciplines</h2>
              <div className="flex flex-wrap gap-2">
                {profile.disciplines.map((discipline, index) => (
                  <span 
                    key={index}
                    className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                  >
                    {discipline}
                  </span>
                ))}
              </div>
            </div>
          )}

          {profile.research_interests && (
            <div className="mt-6">
              <h2 className="text-xl font-semibold mb-2">Research Interests</h2>
              <p className="text-gray-700">{profile.research_interests}</p>
            </div>
          )}

          <div className="mt-6 grid grid-cols-2 gap-4">
            {profile.office_location && (
              <div>
                <h3 className="font-semibold">Office Location</h3>
                <p className="text-gray-700">{profile.office_location}</p>
              </div>
            )}
            {profile.office_hours && (
              <div>
                <h3 className="font-semibold">Office Hours</h3>
                <p className="text-gray-700">{profile.office_hours}</p>
              </div>
            )}
          </div>
        </div>

        {projects.length > 0 && (
          <div className="mt-8">
            <h2 className="text-2xl font-bold mb-4">Supervised Projects</h2>
            <div className="space-y-4">
              {projects.map((project) => (
                <div key={project.id} className="bg-white rounded-lg shadow p-4">
                  <Link 
                    to={`/projects/${project.slug}`}
                    className="text-lg font-semibold text-blue-600 hover:text-blue-800"
                  >
                    {project.title}
                  </Link>
                  <p className="text-gray-600 mt-1">
                    {project.author_name} • {project.degree_type} • {project.academic_year}
                  </p>
                  {project.abstract && (
                    <p className="text-gray-700 mt-2 line-clamp-3">{project.abstract}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
};
