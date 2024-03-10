import './style.css'
import { Browse } from './pages/Browse';
import { Footer } from './components/Footer';
import { Main } from './pages/Main';
import { Resister } from './pages/Resister';
import { BrowserRouter as Router, Route, Routes} from "react-router-dom";
import { Navi } from './Navi';
import 'bootstrap/dist/css/bootstrap.min.css';
import { GetClass } from './pages/GetClass';
import { GetPeople } from './pages/GetPeople';
function App() {
  return (
    <div className='App'>
      <Router>
        <Navi/>
        <div id='contents'>
          <Routes>
          <Route path='/browse' element={<Browse/>}/>
          <Route path='/register' element={<Resister/>}/>
          <Route path='/getclass' element={<GetClass/>}/>
          <Route path='/getpeople' element={<GetPeople/>}/>
          <Route path='/' element={<Main/>}/>
          <Route path='*' element={<Main/>}/>
        </Routes>
        </div>
        <Footer/>
      </Router>
    </div>
  );
}

export default App;
