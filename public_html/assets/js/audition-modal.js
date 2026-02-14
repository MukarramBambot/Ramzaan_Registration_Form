/**
 * Audition Modal Component
 */

function getMediaFileType(filePath, backendType) {
    const videoExtensions = ['mp4', 'webm', 'mov', 'ogg', 'mkv', 'avi'];
    const extension = filePath.split('.').pop()?.toLowerCase() || '';

    if (videoExtensions.includes(extension)) return 'video';
    if (['mp3', 'wav', 'm4a', 'aac', 'flac'].includes(extension)) return 'audio';

    return backendType;
}

function openAuditionModal(file) {
    const container = document.getElementById('audition-modal-container');
    if (!container) return;

    // file: { url, name, type (audio|video) }

    // Fallback logic for type
    const mediaType = getMediaFileType(file.url, file.type);

    const contentHTML = `
        <div class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6 animate-fadeIn transition-opacity">
            <div class="absolute inset-0 bg-black/60 backdrop-blur-md" onclick="closeAuditionModal()"></div>

            <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-4xl overflow-hidden transform transition-all scale-100 animate-zoomIn">
                <!-- Header -->
                <div class="bg-[#112D4E] px-6 py-4 flex items-center justify-between">
                    <div class="flex items-center gap-3">
                        ${mediaType === 'audio'
            ? `<svg class="w-5 h-5 text-[#3F72AF]" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 22h.5c.5 0 1-.5 1-1V7c0-.5-.5-1-1-1h-.5L9 2H2v20h15.5z"></path></svg>` // FileAudio placeholder
            : ICONS.video.replace('class="', 'class="w-5 h-5 text-indigo-400 ') // Reuse main.js icon if possible or inline
        }
                        <h3 class="text-white font-medium truncate max-w-[200px] sm:max-w-md">
                            ${file.name}
                        </h3>
                    </div>
                    <button onclick="closeAuditionModal()" class="p-2 text-[#DBE2EF] hover:text-white hover:bg-white/10 rounded-full transition-all">
                        ${ICONS.x}
                    </button>
                </div>

                <!-- Player -->
                <div class="p-4 sm:p-8 bg-[#F9F7F7] flex flex-col items-center justify-center min-h-[300px] sm:min-h-[350px]">
                    ${mediaType === 'audio'
            ? `
                        <div class="w-full max-w-2xl space-y-8 py-4">
                            <div class="w-32 h-32 bg-[#DBE2EF] rounded-full flex items-center justify-center mx-auto shadow-inner ring-4 ring-white">
                                ${ICONS.play.replace('<svg', '<svg class="w-14 h-14 text-[#3F72AF] fill-current"')}
                            </div>
                            <audio controls autoPlay src="${file.url}" class="w-full h-14" controlsList="nodownload">
                                Your browser does not support the audio element.
                            </audio>
                            <div class="flex justify-center flex-col items-center gap-2">
                                <p class="text-center text-[#112D4E] font-medium">Audio Audition</p>
                                <p class="text-center text-[#6B7280] text-sm">Streaming media securely from server</p>
                            </div>
                        </div>
                        `
            : `
                        <div class="w-full flex flex-col items-center gap-6">
                            <div class="relative group w-full bg-black rounded-xl overflow-hidden shadow-2xl flex items-center justify-center border-4 border-white">
                                <video controls autoPlay src="${file.url}" class="max-h-[60vh] w-full" controlsList="nodownload">
                                    Your browser does not support the video element.
                                </video>
                            </div>
                            <p class="text-[#6B7280] text-sm flex items-center gap-2 bg-white px-4 py-2 rounded-full shadow-sm border border-[#DBE2EF]">
                                <svg class="w-4 h-4 text-indigo-600" xmlns="http://www.w3.org/2000/svg" width="24" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"></polygon><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg>
                                Streaming high-quality video...
                            </p>
                        </div>
                        `
        }
                </div>

                <!-- Footer -->
                <div class="bg-white px-6 py-4 border-t border-[#DBE2EF] flex justify-end">
                    <button onclick="closeAuditionModal()" class="px-8 py-2.5 bg-[#112D4E] text-white rounded-lg hover:bg-[#2D5A8F] transition-all font-medium text-sm shadow-md">
                        Done Previewing
                    </button>
                </div>
            </div>
        </div>
    `;

    container.innerHTML = contentHTML;
    if (typeof ScrollLockManager !== 'undefined') {
        ScrollLockManager.lock();
    } else {
        document.body.style.overflow = 'hidden';
    }
}

function closeAuditionModal() {
    const container = document.getElementById('audition-modal-container');
    if (container) {
        container.innerHTML = '';
        if (typeof ScrollLockManager !== 'undefined') {
            ScrollLockManager.unlock();
        } else {
            document.body.style.overflow = 'unset';
        }
    }
}
