from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast_video_update(video_id, event_type, payload):
    layer = get_channel_layer()
    if layer is None:
        return

    async_to_sync(layer.group_send)(
        f"video_{video_id}",
        {
            "type": "video.update",
            "data": {"event": event_type, "video_id": video_id, **payload},
        },
    )