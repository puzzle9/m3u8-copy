"""M3u8Hls Migration."""

from masoniteorm.migrations import Migration

from app.Models.M3u8Hls import M3u8Hls as M3u8HlsModel


class M3u8Hls(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("m3u8_hls") as table:
            table.increments("id")
            table.integer("m3u8_list_id").unsigned().index("m3u8_list_id")
            table.integer("duration").unsigned()
            table.string("url")
            table.string("path").index("path")
            table.string("status").index("status")
            table.string("key").nullable()

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("m3u8_hls")
