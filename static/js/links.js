/**
 * Created by Samuel on 11/7/2016
 */
$(function () {
    // variable declarations
    var obj = this; // give reference
    var $filesTable = $('#files-table');
    var $links = $('#links');
    var $information = $('#information');
    this.$selected = $(); // jquery equivalent null

    window.fileElement = '<tr class="file">' +
        '<th class="user"><a href="/pages/dashboard#{memberId}">{user}</a></th>' +
        '<th class="path"><a href="{url}">{path}</a></th>' +
        '<th class="access">{access}</th>' +
        '<th class="age" style="color: {ageColor}">{age}</th>' +
        '</tr>';
    this.updateContents = function () {

        $.ajax({
            dataType: 'json',
            url: '/links',
            success: function(members) {
                $links.html('');
                members.forEach(function (member) {
                    member.links.forEach(function (link) {
                        var $linkElement = $(fileElement.format(obj.processLink(member, link))).data('link', obj.processLink(member, link));
                        $links.append($linkElement);
                    });
                });

                $filesTable.show(); // reveal files after load
                obj.linkListeners();
            }
        })
    };

    this.listeners = function () {

    };

    var emptyInfo = {
        'user': '',
        'path': '',
        'access': '',
        'url': '',
        'linkDate': '',
        'memberId': '',
        'age': ''
    };
    this.linkListeners = function () {
        $('.file', $links).on('click', function () {
            obj.$selected.removeClass('active');
            obj.updateInfo(emptyInfo);
            if (obj.$selected[0] != this) {
                $(this).toggleClass('active');
                obj.updateInfo($(this).data('link'));
            }

            obj.$selected = $(this);
        });
    };

    // requires path, url, link date, expiration
    this.processLink = function (member, file) {
        var data = {};

        data.user = member.display_name;
        data.memberId = member.team_member_id;
        data.path = file.path;
        data.access = file.access_type;
        data.url = file.preview_url;
        data.linkDate = file.time_invited;

        data.age = file.days_old;
        data.ageColor = 'ForestGreen';
        if (data.age >= 180)
            data.ageColor = 'Crimson';
        else if (data.age >= 90)
            data.ageColor = 'Coral';

        return data;
    };


    this.updateInfo = function (info) {
        console.log('updated with', info);

        $('.user', $information).text(info.user);
        $('.member_id', $information).text(info.memberId);
        $('.path', $information).text(info.path);
        $('.access', $information).text(info.access);
        $('.url', $information).attr('href', info.url);
        $('.url', $information).text(info.url);
        $('.linkDate', $information).text(info.linkDate);
        $('.age', $information).text(info.age);
    };

    // run initial methods
    obj.updateContents();
    obj.listeners();
});