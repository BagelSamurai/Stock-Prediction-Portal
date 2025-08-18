import { useState } from 'react'

import './assets/css/style.css'
import Header from "./components/Header.jsx";
import Footer from "./components/Footer.jsx";
import Dashboard from "./components/Dashboard.jsx";


function App() {


  return (
      <>
          <Header/>
         <Dashboard/>
          <Footer/>
      </>
  )
}

export default App
