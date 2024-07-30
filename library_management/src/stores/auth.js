import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import Cookies from 'js-cookie';

export const auth = defineStore('auth', () => {
    const backend_url = 'http://127.0.0.1:5000';
    const token = ref(localStorage.getItem('token')); // Removed computed() wrapper
    const user_details = ref(localStorage.getItem('user_details') ? JSON.parse(localStorage.getItem('user_details')) : null); // Removed computed() wrapper and added JSON parsing

    const username = computed(() => user_details.value?.username || '');
    const role = computed(() => user_details.value?.role || '');

    const isAuthenticated = computed(() => token.value !== null);

    function updateToken(){
        token.value=localStorage.getItem("token")
    }
    function updateUserDetails(){
        user_details.value=localStorage.getItem("user_details")
    }

    function setToken(newToken) {
        localStorage.setItem('token', newToken);
        token.value = newToken; // Update reactive token
    }

    function removeToken() {
        localStorage.removeItem('token');
        token.value = null; // Update reactive token
    }

    function removeUserDetails() {
        localStorage.removeItem('user_details');
        user_details.value = null; // Update reactive user_details
    }

    function setUserDetails(details) {
        localStorage.setItem('user_details', JSON.stringify(details));
        user_details.value = details; // Update reactive user_details
    }

    async function logout() {
        try {
            const response = await fetch(`${backend_url}/api/v1/logout`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Authentication-Token': token.value,
                },
            });

            if (!response.ok) {
                const data = await response.json();
                const rsp = {
                    status: false,
                    message: data.message,
                };
                return rsp;
            } else {
                const data = await response.json();
                const rsp = {
                    status: true,
                    message: data.message,
                };
                removeToken();
                removeUserDetails();
                //window.location.reload(); // Page reload on logout
                return rsp;
            }
        } catch (error) {
            console.error(error);
            const rsp = {
                status: false,
                message: 'Oops! Something Went Wrong',
            };
            return rsp;
        }
    }

    async function login(user_details) {
        try {
            const response = await fetch(`${backend_url}/api/v1/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                body: JSON.stringify(user_details),
            });

            if (!response.ok) {
                const data = await response.json();
                const rsp = {
                    status: false,
                    message: data.message,
                };
                return rsp;
            } else {
                const data = await response.json();
                if (data.user.auth_token) {
                    Cookies.set('SECURITY_TOKEN_AUTHENTICATION_HEADER', data.user.auth_token, { expires: 7 });
                    setToken(data.user.auth_token);
                    const user_dets = {
                        username: data.user.username,
                        role: data.user.roles[0],
                        email: data.user.email,
                    };
                    setUserDetails(user_dets);

                    const rsp = {
                        status: true,
                        message: data.message,
                    };
                    //window.location.reload(); // Page reload on login
                    return rsp;
                }
            }
        } catch (error) {
            console.error(error);
            const rsp = {
                status: true,
                message: 'Oops! Something Went Wrong',
            };
            return rsp;
        }
    }

    async function register(user_details) {
        try {
            const response = await fetch(`${backend_url}/api/v1/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                body: JSON.stringify(user_details),
            });

            if (!response.ok) {
                const data = await response.json();
                const rsp = {
                    status: false,
                    message: data.message,
                };
                return rsp;
            } else {
                const data = await response.json();
                const rsp = {
                    status: true,
                    message: data.message,
                };
                return rsp;
            }
        } catch (error) {
            console.error(error);
            const rsp = {
                status: false,
                message: 'Oops! Something Went Wrong',
            };
            return rsp;
        }
    }

    return { login, logout, register, token, username, isAuthenticated, backend_url, role ,updateToken,updateUserDetails};
});
