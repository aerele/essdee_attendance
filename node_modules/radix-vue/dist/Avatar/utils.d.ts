import { Ref } from 'vue';
export type ImageLoadingStatus = 'idle' | 'loading' | 'loaded' | 'error';
export declare function useImageLoadingStatus(src: Ref<string>): Ref<ImageLoadingStatus>;
