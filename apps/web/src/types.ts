import type {JSONContent} from '@tiptap/core';
import type {MessageParams} from '../../../packages/i18n/core';
export type User={id:string;email:string;name:string;locale?:string|null};
export type Canonical={schemaVersion:2;language:string;direction:'auto'|'ltr'|'rtl';content:JSONContent};
export type Project={id:string;title:string;language:string;direction:'auto'|'ltr'|'rtl';version:string;access_epoch:number;role:'owner'|'editor'|'viewer';updated_at:string;chapterCount?:number;chapters:{id:string;title:string;position:number;revisionId:string}[]};
export type Chapter={id:string;title:string;projectId:string;revisionId:string;sequence:number;savedAt:string;accessEpoch:number;ast:Canonical;role:Project['role']};
export type Revision={id:string;sequence:number;createdAt:string;restoredFrom:string|null;actorName:string};
export type ImportPreview={id:string;reportHash:string;warnings:{id:string;message:string;messageKey?:string;messageParams?:MessageParams}[];textPreview:string};
