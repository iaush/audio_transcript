import React, {useState, useEffect} from 'react';
import api from '../services/api';


const Health = () => {
    const [status, setStatus] = useState(false);

    useEffect(()=>{
        const status = async()=>{
            try{
                const response = api.get('/status').then((response)=>{
                    if (response.status === 200){
                        setStatus(true);
                    }
                }).catch((error)=>{
                    setStatus(false);
                })
            }catch(error){
                setStatus(false);
            }
        }
        status();
        const interval = setInterval(status,10000)

        return () => clearInterval(interval)
    },[])

  return (
    <div style={{ position: "absolute", top: 10, right: 10, fontSize: "14px", color: status ? "green" : "red" }}>
      API Status : {status ? "Online" : "Offline"}
    </div>
  );
};

export default Health;