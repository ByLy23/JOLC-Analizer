import React from 'react';
import '../css/analizador.css';
import CodeMirror from '@uiw/react-codemirror';
import 'codemirror/theme/monokai.css';
import 'codemirror/keymap/sublime';
export const Analizador = () => {
  const code = 'const a=0';
  const salida = 'Output> asdasd';
  return (
    <div className="analizer-container">
      <div className="analizer animate__animated animate__fadeInUp">
        <div className="analizer-card">
          <input type="submit" className="analizar" value="Analizar" />
          <div className="editor">
            <CodeMirror
              value={code}
              options={{
                theme: 'monokai',
                keyMap: 'sublime',
                mode: 'julia',
                viewportMargin: Infinity,
                autofocus: false,
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
    </div>
  );
};
