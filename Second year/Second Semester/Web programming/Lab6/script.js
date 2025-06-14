$(document).ready(function () {
    const desktops = $('.desktop');
    let currentIndex = 0;

    desktops.hide().eq(currentIndex).css({ top: '0', left: '0' }).show();

    $('body').on('click', function () {
        const current = desktops.eq(currentIndex);
        currentIndex = (currentIndex + 1) % desktops.length;
        const next = desktops.eq(currentIndex);

        next.css({ top: '0', left: '100vw', display: 'block' });

        current.animate({ left: '-100vw' }, 600, function () {
            $(this).css({ top: '0', left: '0', display: 'none' });
        });

        next.animate({ left: '0' }, 600);
    });
});
