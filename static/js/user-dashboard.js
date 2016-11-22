/**
 * Created by samuel on 11/19/16.
 */

$(function () {
    var obj = this;
    this.name = url('?name');
    this.teamMemberId = url('?member-id');
    var $shared = $('#shared-table');
    var $links = $('#links-table');

    console.log(url('query'));
    console.log('ID', obj.teamMemberId);
    console.log('Name', obj.name);

    obj.updateShared = function () {
        // get shared
        $.ajax({
            'url': '/members/{teamMemberId}/shared-folders'.format({
                teamMemberId: obj.teamMemberId
            }),
            'method': 'GET',
            'dataType': 'json',
            success: function (shared) {
                console.log('Retreieved Shared', shared);

                obj.displayShared(shared);
            }
        });
    };

    obj.updateLinks = function () {
        // get links
        $.ajax({
            'url': '/members/{teamMemberId}/shared-links'.format({
                teamMemberId: obj.teamMemberId
            }),
            'method': 'GET',
            'dataType': 'json',
            success: function (links) {
                console.log('Retreieved Links', links);

                obj.displayLinks(links);
            }
        });
    };

    var shareHtml = '<tr>' +
        '<th>{access}</th>' +
        '<th>{name}</th>' +
        '<th><a href="{url}" target="_blank">{path}</a></th>' +
        '<th style="color: {daysColor}">{days}</th>' +
        '<th>{invited}</th>' +
        '<th>{sharedFolderId}</th></tr>';
    this.displayShared = function (shared) {
        $shared.html(''); // clean

        shared.forEach(function (share) {
            var $shareElement = $(shareHtml.format(obj.processShared(share)));

            $shared.append($shareElement);
        });
    };

    this.processShared = function (share) {
        var data = {};

        data.access = share.access_type;
        data.name = share.name;
        data.url = share.preview_url;
        data.path = share.path;

        data.days = share.days_old;
        data.daysColor = 'ForestGreen';
        if (data.days >= 180)
            data.daysColor = 'Crimson';
        else if (data.days >= 90)
            data.daysColor = 'Coral';

        data.invited = share.time_invited;
        data.sharedFolderId = share.shared_folder_id;

        return data;
    };

    var linksElement = '<tr class="link">' +
        '<th class="revoke-cell"><button class="btn btn-warning btn-xs revoke-link {revoke}">Revoke</button></th>' +
        '<th>{name}</th>' +
        '<th>{expiration}</th>' +
        '<th><a href="{url}" target="_blank">{path}</a></th>' +
        '<th>{visible}</th></tr>';
    this.displayLinks = function (links) {
        $links.html(''); // clean

        links.forEach(function (link) {
            var $linkElement = $(linksElement.format(obj.processLink(link)));

            $linkElement.hover(function () {
                $(this).find('.revoke-link').show();
            }, function () {
                $(this).find('.revoke-link').hide();
            });

            $linkElement.find('.revoke-link').on('click', obj.revokeLink).data('url', link.url).data('member-id', obj.teamMemberId);

            $links.append($linkElement);
        });
    };

    this.revokeLink = function () {
        if (!$(this).hasClass('disabled')) {
            var url = $(this).data('url');
            var memberId = $(this).data('member-id');

            $('#revoke-confirm-modal').modal();
            $('#confirm-revoke').one('click', function () {
                $.ajax({
                    method: 'DELETE',
                    url: '/members/{memberId}/shared-links/{url}'.format({
                        url: url,
                        memberId: memberId
                    }),
                    success: function () {
                        obj.updateLinks();
                        console.log('Revoke Successful');
                    }
                });
            });
        }
    };

    this.processLink = function (link) {
        var data = {};

        data.revoke = link.can_revoke ? '' : 'disabled';

        data.name = link.name;
        data.path = link.path;
        data.url = link.url;

        data.expiration = link.expires;
        if (link.expires == null)
            data.expiration = 'Never';

        data.visible = link.visibility;

        return data;
    };

    if (obj.teamMemberId && obj.name) {
        $('#member-name').text(obj.name);
        $('#team-member-id').text(obj.teamMemberId);

        obj.updateShared();
        obj.updateLinks();
    }
    else {
        $('#no-id-modal').modal();
    }
});