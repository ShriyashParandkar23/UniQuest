import React from 'react'
import LandingPage from '../pages/LandingPage'
import { Routes, Route } from 'react-router-dom';
import Dashboard from '../pages/Dashboard';
import AIChatAssistant from '../pages/AIChatAssistant';


const App = () => {

  return (
    <Routes>
         

    <Route path='/' element={<LandingPage/>}/>
          <Route path='/dashboard' element={<Dashboard/>}/>
    <Route path='/ai-chat' element={<AIChatAssistant/>}/>


    </Routes>
 
  )
}

export default App