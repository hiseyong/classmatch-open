import axios from "axios"
import { useState, useEffect } from "react"
import emailjs from '@emailjs/browser';
export function GetPeople() {
    const client = axios.create()
    const [userInfo, setUserInfo] = useState({
      'year' : ''
    })
    useEffect(() => {
      emailjs.init('94a1FVAHS5Bi638pb');
    }, []);
    const [rec, setRec] = useState([])
    const [classes, setClasses] = useState(null)
    const [msg, setMsg] = useState('')
    const [btnTxt, setBtnTxt] = useState('가입자 조회하기')
  
  
    const onClick = () => {
      setBtnTxt('로딩중...')
      client.post('https://api.hasclassmatching.com/api/getpeople', userInfo)
      .then(res=>{
        setBtnTxt('가입자 조회하기')
        if(typeof(res.data) === 'string') {
          setRec([])
          setMsg(res.data)
        } else {
          if (res.data.length === 0) {
            setMsg(['해당 학년의 가입자가 없습니다'])
            setRec([])
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
    return(
        <div id='contain'>
            <h3>가입자 조회하기</h3>
            <input placeholder='조회하려는 학년의 고유학번 앞 두자리' id='in' onChange={onChange} name='year'/>
            <button variant="primary" type="submit" onClick={onClick} id='btn'>
                {btnTxt}
            </button>
            <br/>
            <label id='err'>{msg}</label>
            <br/>
            <h3>총 {rec.length}명</h3>
            <div id="peoplediv">
                {rec.map((elem)=><h5>{elem[0]+' '+elem[1]}</h5>)}
            </div>
        </div>
    )
}