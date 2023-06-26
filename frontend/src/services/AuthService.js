import axios from 'axios';
import { AUTH_API_BASE_URL } from '../utils/Consts';


const apiClient = axios.create({
    baseURL: AUTH_API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});


export const login = async (email, password) => {
    try {
        const response = await apiClient.post('/api/v1/token/', { email, password });
        return response.data;
    } catch (error) {
        if (error.response && error.response.data && error.response.data.detail) {
            throw new Error(error.response.data.detail);
        } else {
            throw new Error('Возникла ошибка при входе!');
        }
    }
};