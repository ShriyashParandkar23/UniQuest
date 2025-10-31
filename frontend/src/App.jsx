import React from 'react'
import LandingPage from '../pages/LandingPage'
import { Routes, Route } from 'react-router-dom';
import Dashboard from '../pages/Dashboard';
import AIChatAssistant from '../pages/AIChatAssistant';
import Login from '../pages/Login';
import UserProfilePage from '../pages/UserProfilePage';
import { UserProfile } from '@clerk/clerk-react';



const App = () => {

  return (
    <Routes>
         

    <Route path='/' element={<LandingPage/>}/>
    <Route path='/dashboard' element={<Dashboard/>}/>
    <Route path='/ai-chat' element={<AIChatAssistant/>}/>
    <Route path='/login' element={ <Login/> }/>
    <Route path='/UserProfile' element={ <UserProfilePage/> }/>


    </Routes>
 
  )
}

export default App