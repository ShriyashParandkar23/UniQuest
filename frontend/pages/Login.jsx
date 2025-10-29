import React, { useEffect } from 'react'
import { SignIn, useUser } from '@clerk/clerk-react'
import { useNavigate } from 'react-router-dom'
import Header from '../components/Header'
import Dashboard from './Dashboard'

export default function Login() {
    const { isLoaded, isSignedIn, user } = useUser()
    const navigate = useNavigate()
    //console.log(isLoaded, isSignedIn, user.firstName)

    useEffect(() => {
    if (isLoaded && isSignedIn) {
        console.log(user.firstName)
      navigate('/dashboard', { replace: true })
    }
  }, [isLoaded, isSignedIn, navigate])
    return (
        <>
        <Header />
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <div className="w-full max-w-md p-6">
            <SignIn path="/login" routing="path" />
        </div>
      </div>
    </>
    )
}