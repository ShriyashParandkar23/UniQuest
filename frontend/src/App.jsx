import React from 'react'
import LandingPage from '../pages/LandingPage'
import { Routes, Route } from 'react-router-dom';
import Dashboard from '../pages/Dashboard';


const App = () => {

  return (
    <Routes>
         

    <Route path='/' element={<LandingPage/>}/>
    <Route path='/dashboard' element={<Dashboard/>}/>

    </Routes>
 
  )
}

export default App