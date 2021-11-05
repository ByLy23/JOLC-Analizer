import React, { useState } from 'react';
import '../css/analizador.css';
import 'codemirror/theme/cobalt.css';
import 'codemirror/keymap/sublime';
import { PopupAn } from '../components/PopupAn';
import { CodeMirrorComponent } from '../components/CodeMirrorComponent';
import { getConsola } from '../helpers/getConsola';
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
  const [salida = { outputCode: 'salida' }, setSalida] = useState({ outputCode: JSON.parse(localStorage.getItem('SALIDA_CONSOLA')) });

  const valor = {
    estado: state.outputCode,
    colocaEstado: setstate,
  };
  const handleSubmit = () => {
    getConsola(valor).then(({ consola, simbolos, errores, ast }) => {
      localStorage.setItem('SALIDA_CONSOLA', JSON.stringify(consola));
      localStorage.setItem('TABLA_SIMBOLOS', JSON.stringify(simbolos));
      localStorage.setItem('TABLA_ERRORES', JSON.stringify(errores));
      localStorage.setItem('EDITOR', JSON.stringify(valor.estado));
      localStorage.setItem('ARBOL_AST', JSON.stringify(ast));
      setSalida({ outputCode: consola });
      setpopUp(true);
    });
  };
  // useEffect(() => {
  //   getPokemons('ditto').then(({ abilities }) => setpokemon(abilities));
  //   console.log(pokemon);
  // }, [pokemon]);

  const input = <input type="submit" className="analizar" onClick={handleSubmit} value="Traducir" />;

  const label = React.createElement('h1', { className: 'con-text' }, 'Consola');
  return (
    <div className="analizer-container">
      <CodeMirrorComponent input={input} codeMirrorValue={valor} writable="true" clase="editor" modo="julia" />
      <CodeMirrorComponent input={label} codeMirrorOut={salida.outputCode} writable="false" clase="console" modo="go" />
      {popUp && <PopupAn setpopUp={setpopUp} valor={'Traducido'} />}
    </div>
  );
};
