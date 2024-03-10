import axios from "axios"
import { useState,useEffect } from "react"
import emailjs from '@emailjs/browser';

export function Browse() {
    const client = axios.create()
    const [userInfo, setUserInfo] = useState({
      'year':'',
      'id1' : '',
      'id2' : ''
    })
    
    useEffect(() => {
      emailjs.init('94a1FVAHS5Bi638pb');
    }, []);
    const [rec, setRec] = useState([])
    const [msg, setMsg] = useState('')
    const [btnTxt, setBtnTxt] = useState('겹치는 과목 조회하기')
  
  
    const onClick = () => {
      setBtnTxt('로딩중...')
      client.post('https://api.hasclassmatching.com/api/match', userInfo)
      .then(res=>{
        setBtnTxt('겹치는 과목 조회하기')
        if(typeof(res.data) === 'string') {
          setRec([])
          setMsg(res.data)
        } else {
          if (res.data.length === 0) {
            setRec(['겹치는 과목이 없습니다'])
          } else {
            setMsg('')
            setRec(res.data)
          }
          
        }
      })
      .catch(err=>{
        setMsg('예기치 못한 에러 발생')
        setBtnTxt('겹치는 과목 조회하기')
        emailjs.send('service_879kgqu', 'template_y2r986d', {});
      })
    }
  
    
    const onChange = (e) => {
      setUserInfo({
        ...userInfo,
        [e.target.name] : e.target.value
      })
    }
  
    return (
        <div id='contain'>
          <h3>겹치는 과목 조회하기</h3>
          <input placeholder="고유학번 앞 두자리" onChange={onChange} name="year" id="in"/>
          <input placeholder='이름1' id='in' onChange={onChange} name='id1'/>
          <br/>
          <input placeholder='이름2' id='in' onChange={onChange} name='id2'/>
          <button variant="primary" type="submit" onClick={onClick} id='btn'>
              {btnTxt}
          </button>
          <br/>
          <label id='err'>{msg}</label>
          <br/>
          <h5>{rec.map((elem) => (elem+', '))}</h5>
        </div>
    );
  }