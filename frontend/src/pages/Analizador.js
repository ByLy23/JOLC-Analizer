import React, { useState } from 'react';
import '../css/analizador.css';
import CodeMirror from '@uiw/react-codemirror';
import 'codemirror/theme/monokai.css';
import 'codemirror/keymap/sublime';
import { PopupAn } from '../components/PopupAn';
export const Analizador = () => {
  const salida = 'Output>asdad';
  const [state = { outputCode: 'salida' }, setstate] = useState([]);
  const [popUp, setpopUp] = useState(false);
  const handleSubmit = () => {
    console.log(state);
    setpopUp(true);
  };
  return (
    <div className="analizer-container">
      <div className="analizer animate__animated animate__fadeInUp">
        <div className="analizer-card">
          <input
            type="submit"
            className="analizar"
            onClick={handleSubmit}
            value="Analizar"
          />
          <div className="editor">
            <CodeMirror
              value={state.outputCode}
              options={{
                theme: 'monokai',
                keyMap: 'sublime',
                mode: 'julia',
                viewportMargin: Infinity,
                autofocus: false,
              }}
              onChange={(editor, data, value) => {
                setstate({
                  outputCode: editor.getValue(),
                });
              }}
            />
          </div>
        </div>
      </div>

      <div className="consola animate__animated animate__fadeInUp">
        <div className="analizer-card">
          <h1 className="con-text">Consola</h1>
          <div className="console">
            <CodeMirror
              value={salida}
              options={{
                theme: 'monokai',
                keyMap: 'sublime',
                mode: 'julia',
                viewportMargin: Infinity,
                readOnly: true,
                autofocus: false,
              }}
            />
          </div>
        </div>
      </div>
      {popUp && <PopupAn setpopUp={setpopUp} valor={'Analizado'} />}
    </div>
  );
};
