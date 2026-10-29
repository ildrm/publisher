import {useCallback,useEffect,useRef,useState} from 'react';
import {EditorContent,useEditor,useEditorState} from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import {Extension,type JSONContent} from '@tiptap/core';
import {Plugin} from '@tiptap/pm/state';
import type {EditorView} from '@tiptap/pm/view';
import type {Canonical} from './types';
import {useI18n} from '../../../packages/i18n/index';

const blocks=['paragraph','heading','blockquote','bulletList','orderedList','listItem','horizontalRule'];
const StableIds=Extension.create({name:'stableIds',addGlobalAttributes(){return [{types:blocks,attributes:{id:{default:null,parseHTML:element=>element.getAttribute('data-block-id'),renderHTML:attributes=>({'data-block-id':attributes.id})}}}];},addProseMirrorPlugins(){return [new Plugin({appendTransaction:(_transactions,_old,state)=>{const seen=new Set<string>();const tr=state.tr;let changed=false;state.doc.descendants((node,pos)=>{if(!blocks.includes(node.type.name))return;let id=node.attrs.id as string|null;if(!id||seen.has(id)){id=crypto.randomUUID();tr.setNodeMarkup(pos,undefined,{...node.attrs,id});changed=true;}seen.add(id);});return changed?tr:null;}})];}});
export const extensions=[StarterKit.configure({heading:{levels:[1,2,3]},codeBlock:false,underline:false,link:{openOnClick:false,autolink:false,linkOnPaste:false}}),StableIds];

export function ManuscriptEditor({initial,editable,onChange,onEditorReady}:{initial:Canonical;editable:boolean;onChange:(ast:Canonical)=>void;onEditorReady?:(get:()=>Canonical)=>void}){
  const {t,locale}=useI18n();const tRef=useRef(t);tRef.current=t;
  const initialRef=useRef(initial);const callback=useRef(onChange);callback.current=onChange;
  const [pasteWarning,setPasteWarning]=useState('');
  const [direction,setDirection]=useState(initial.direction);const directionRef=useRef(direction);directionRef.current=direction;
  const [lang,setLang]=useState(initial.language);const langRef=useRef(lang);langRef.current=lang;
  const handlePaste=useCallback((_view:EditorView,event:ClipboardEvent)=>{const html=event.clipboardData?.getData('text/html')??'';if(/<(table|img|svg|sup|iframe)\b|footnote|endnote/i.test(html)){setPasteWarning('This paste contains tables, images or notes that this editor does not support yet. Import the DOCX file to review transformations, or paste supported text only.');return true;}setPasteWarning('');return false;},[]);
  const editor=useEditor({extensions,content:initial.content,editable,injectCSS:false,
    editorProps:{handlePaste,attributes:{role:'textbox','aria-label':tRef.current('Manuscript content'),'aria-multiline':'true',spellcheck:'true',translate:'no',dir:direction,lang}},
    onUpdate:({editor,transaction})=>{if(editor.isEditable&&transaction.docChanged)callback.current({...initialRef.current,language:langRef.current,direction:directionRef.current,content:editor.getJSON()});}},[]);
  const state=useEditorState({editor,selector:({editor})=>({bold:editor?.isActive('bold'),italic:editor?.isActive('italic'),quote:editor?.isActive('blockquote'),bullet:editor?.isActive('bulletList'),ordered:editor?.isActive('orderedList'),heading:editor?.getAttributes('heading').level as number|undefined,text:editor?.getText()??''})});
  const [words,setWords]=useState(0);
  useEffect(()=>{const timer=setTimeout(()=>{let count=0;const text=state?.text??'';if(typeof Intl.Segmenter==='function'){let segmenter:Intl.Segmenter;try{segmenter=new Intl.Segmenter(lang,{granularity:'word'});}catch{segmenter=new Intl.Segmenter('en',{granularity:'word'});}for(const part of segmenter.segment(text)){if(part.isWordLike)count++;}}else count=text.trim().split(/\s+/u).filter(Boolean).length;setWords(count);},200);return()=>clearTimeout(timer);},[state?.text,lang]);
  useEffect(()=>{editor?.setEditable(editable,false);},[editor,editable]);
  useEffect(()=>{if(editor)onEditorReady?.(()=>({...initialRef.current,direction:directionRef.current,language:langRef.current,content:editor.getJSON()}));},[editor,onEditorReady]);
  // Update accessible chrome without recreating the editor or changing authored metadata.
  useEffect(()=>{editor?.setOptions({editorProps:{handlePaste,attributes:{role:'textbox','aria-label':t('Manuscript content'),'aria-multiline':'true',spellcheck:'true',translate:'no',dir:direction,lang}}});},[editor,direction,lang,t,locale.code,handlePaste]);
  if(!editor)return <p>{t('Opening manuscript…')}</p>;
  const changeMeta=(nextDirection:Canonical['direction'],nextLang:string)=>{setDirection(nextDirection);setLang(nextLang);callback.current({...initialRef.current,direction:nextDirection,language:nextLang,content:editor.getJSON()});};
  const tool=(name:string,active:boolean|undefined,action:()=>void,label=name)=><button type="button" title={t(label)} aria-label={t(label)} aria-pressed={!!active} onClick={action} disabled={!editable}>{name==='B'||name==='I'?name:t(name)}</button>;
  return <>
    {pasteWarning&&<div className="notice warning" role="alert">{t(pasteWarning)}<button className="text-button" onClick={()=>setPasteWarning('')}>{t('Dismiss')}</button></div>}
    <div className="editor-toolbar" role="toolbar" aria-label={t('Text formatting')}>
      <label className="sr-only" htmlFor="text-style">{t('Text style')}</label><select id="text-style" aria-label={t('Text style')} disabled={!editable} value={state?.heading??0} onChange={e=>{const level=Number(e.target.value);if(level)editor.chain().focus().setHeading({level:level as 1|2|3}).run();else editor.chain().focus().setParagraph().run();}}><option value="0">{t('Paragraph')}</option><option value="1">{t('Heading 1')}</option><option value="2">{t('Heading 2')}</option><option value="3">{t('Heading 3')}</option></select>
      <div className="tool-group">{tool('B',state?.bold,()=>editor.chain().focus().toggleBold().run(),'Bold (Control or Command B)')}{tool('I',state?.italic,()=>editor.chain().focus().toggleItalic().run(),'Italic (Control or Command I)')}{tool('Quote',state?.quote,()=>editor.chain().focus().toggleBlockquote().run())}</div>
      <div className="tool-group">{tool('Bullets',state?.bullet,()=>editor.chain().focus().toggleBulletList().run())}{tool('Numbered',state?.ordered,()=>editor.chain().focus().toggleOrderedList().run())}</div>
      <div className="tool-group">{tool('Undo',false,()=>editor.chain().focus().undo().run())}{tool('Redo',false,()=>editor.chain().focus().redo().run())}</div>
      <span className="word-count">{t('{count} words (approx.)',{count:words})}</span>
    </div>
    <div className="manuscript-settings"><label>{t('Language')}<input aria-label={t('Manuscript language')} value={lang} dir="ltr" maxLength={35} disabled={!editable} onChange={e=>changeMeta(direction,e.target.value)}/></label><label>{t('Text direction')}<select value={direction} disabled={!editable} onChange={e=>changeMeta(e.target.value as Canonical['direction'],lang)}><option value="auto">{t('Automatic')}</option><option value="ltr">{t('Left to right')}</option><option value="rtl">{t('Right to left')}</option></select></label></div>
    <div className="paper" translate="no"><EditorContent editor={editor}/></div>
  </>;
}
export function DocumentPreview({content,language='en',direction='auto'}:{content:JSONContent;language?:string;direction?:Canonical['direction']}){const {t}=useI18n();const editor=useEditor({extensions,content,editable:false,injectCSS:false,editorProps:{attributes:{'aria-label':t('Revision preview'),translate:'no',dir:direction,lang:language}}},[content]);useEffect(()=>{editor?.setOptions({editorProps:{attributes:{'aria-label':t('Revision preview'),translate:'no',dir:direction,lang:language}}});},[editor,t,direction,language]);return <div className="revision-preview" translate="no"><EditorContent editor={editor}/></div>;}
