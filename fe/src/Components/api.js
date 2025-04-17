import axios from "axios";
import { ACCESS_TOKEN } from "../constant";

const apiUrl = "/choreo-apis/awbo/backend/rest-api-be2/v1.0";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : apiUrl,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
export const getDoctors = async () => {
  try {
    const response = await api.get('/api/doctors/');
    return response.data;  
  } catch (error) {
    console.error('Error: ', error);
    return [];  
  }
};
export const createAppointment = async (doctorId, appointmentData) => {
  try {
    const response = await api.post(`/api/appointments/${doctorId}/`, appointmentData);
    return response.data;
  } catch (error) {
    console.error("Error creating appointment:", error);
    throw error;
  }
};
export const getDoctorById = async (doctorId) => {
  try {
    const response = await api.get(`/api/doctors/${doctorId}/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching doctor details:", error);
    throw error;
  }
};
export default api;