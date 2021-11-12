import React, { useState } from 'react';
import '../css/analizador.css';
import 'codemirror/theme/cobalt.css';
import 'codemirror/keymap/sublime';
import { PopupAn } from '../components/PopupAn';
import { getConsola } from '../helpers/getConsola';
import { getOptimizacion } from '../helpers/getOptimizacion';
import CodeMirror from '@uiw/react-codemirror';
import 'codemirror/theme/cobalt.css';
import 'codemirror/keymap/sublime';
export const Analizador = () => {
  const codigo = `for i in 0:9

    output = "";
    for j in 0:(10 - i)
        output = output * " ";
    end;

    for k in 0:i 
        output = output * "* ";
    end;
    println(output);

end;`;
  const [popUp, setpopUp] = useState(false);
  const [state = { outputCode: 'salida' }, setstate] = useState({ outputCode: localStorage.getItem('EDITOR') == null ? codigo : JSON.parse(localStorage.getItem('EDITOR')) });
  const [salida = { outputCode: 'salida' }, setSalida] = useState({ outputCode: localStorage.getItem('SALIDA_CONSOLA') == null ? codigo : JSON.parse(localStorage.getItem('SALIDA_CONSOLA')) });
  const [optimizado = { outputCode: 'salida' }, setoptimizado] = useState({ outputCode: JSON.parse(localStorage.getItem('SALIDA_OPTIMIZADA')) });
  const [texto, settexto] = useState('Traducido');
  const valor = {
    estado: state.outputCode,
    colocaEstado: setstate,
  };
  const optimizar = {
    estado: salida.outputCode,
    colocaEstado: setSalida,
  };
  const handleSubmit = () => {
    getConsola(valor).then(({ consola, simbolos, errores, ast }) => {
      localStorage.setItem('SALIDA_CONSOLA', JSON.stringify(consola));
      localStorage.setItem('TABLA_SIMBOLOS', JSON.stringify(simbolos));
      localStorage.setItem('TABLA_ERRORES', JSON.stringify(errores));
      localStorage.setItem('EDITOR', JSON.stringify(valor.estado));
      localStorage.setItem('ARBOL_AST', JSON.stringify(ast));
      setSalida({ outputCode: consola });
      settexto('Traducido');
      setpopUp(true);
    });
  };
  const handleSumibtOpt = () => {
    localStorage.setItem('SALIDA_CONSOLA', JSON.stringify(salida.outputCode));
    getOptimizacion(optimizar).then(({ consola, simbolos, errores, ast }) => {
      localStorage.setItem('SALIDA_OPTIMIZADA', JSON.stringify(consola));
      localStorage.setItem('TABLA_OPTIMIZACION', JSON.stringify(simbolos));
      setoptimizado({ outputCode: consola });
      settexto('Optimizado');
      setpopUp(true);
    });
  };

  return (
    <div className="analizer-container">
      <div className="analizer animate__animated animate__fadeInUp">
        <div className="analizer-card">
          <input type="submit" className="analizar" onClick={handleSubmit} value="Traducir" />
          <div className="editor">
            <CodeMirror
              value={valor.estado}
              options={{
                theme: 'cobalt',
                keyMap: 'sublime',
                mode: 'julia',
                viewportMargin: Infinity,
                autofocus: false,
                readOnly: false,
              }}
              onChange={(editor, data, value) => {
                valor.colocaEstado({
                  outputCode: editor.getValue(),
                });
                console.log('actualizo');
              }}
            />
          </div>
        </div>
      </div>
      <div className="analizer animate__animated animate__fadeInUp">
        <div className="analizer-card">
          <input type="submit" className="analizar" onClick={handleSumibtOpt} value="Optimizar" />
          <div className="editor">
            <CodeMirror
              value={optimizar.estado}
              options={{
                theme: 'cobalt',
                keyMap: 'sublime',
                mode: 'go',
                viewportMargin: Infinity,
                autofocus: false,
                readOnly: false,
              }}
              onChange={(editor, data, value) => {
                optimizar.colocaEstado({
                  outputCode: editor.getValue(),
                });
                console.log('actualizo');
              }}
            />
          </div>
        </div>
      </div>
      <div className="analizer animate__animated animate__fadeInUp">
        <div className="analizer-card">
          <h1 className="con-text">Consola</h1>
          <div className="console">
            <CodeMirror
              value={optimizado.outputCode}
              options={{
                theme: 'cobalt',
                keyMap: 'sublime',
                mode: 'go',
                viewportMargin: Infinity,
                autofocus: false,
                readOnly: true,
              }}
            />
          </div>
        </div>
      </div>
      {popUp && <PopupAn setpopUp={setpopUp} valor={texto} />}
    </div>
  );
};
