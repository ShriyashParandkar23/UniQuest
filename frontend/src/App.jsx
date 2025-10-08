import React from 'react'
import LandingPage from '../pages/LandingPage'
import { Routes, Route } from 'react-router-dom';
import Dashboard from '../pages/Dashboard';
import Login from '../pages/Login';


const App = () => {

  return (
    <Routes>
         <Route path='/' element={<LandingPage/>}/>
         <Route path='/dashboard' element={<Dashboard/>}/>
         <Route path='/login' element={<Login/>}/>
    </Routes>
 
  )
}

export default App