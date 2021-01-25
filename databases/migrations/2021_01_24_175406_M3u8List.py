"""M3u8List Migration."""

from masoniteorm.migrations import Migration


class M3u8List(Migration):
    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create("m3u8_lists") as table:
            table.increments("id")
            table.string("url").unique()
            table.string("status").index("status")

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("m3u8_lists")
