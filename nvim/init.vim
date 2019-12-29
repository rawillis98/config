nnoremap <buffer> <F9> :exec '!python' shellescape(@%, 1)<cr>

call plug#begin('~/.local/share/nvim/plugged')

Plug 'vim-airline/vim-airline'
Plug 'scrooloose/nerdcommenter'
Plug 'ericbn/vim-relativize'
Plug 'scrooloose/nerdtree'

call plug#end()

set relativenumber

autocmd StdinReadPre * let s:std_in=1
autocmd VimEnter * if argc() == 0 && !exists("s:std_in") | NERDTree | endif
map <C-n> :NERDTreeToggle<CR>


