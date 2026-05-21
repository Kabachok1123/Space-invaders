from typing import Optional

from config import BUNKER_DAMAGE_RADIUS, BUNKER_HIT_PADDING
from models import BunkerBlock, EnemyBullet


def damage_bunker_by_enemy_bullet(bullet: EnemyBullet, blocks: list[BunkerBlock]) -> bool:
    hit_block = find_first_block_on_bullet_path(bullet, blocks)
    if hit_block is None:
        return False

    damage_blocks_near_hit(hit_block, blocks)
    blocks[:] = [block for block in blocks if block.hp > 0]
    return True


def find_first_block_on_bullet_path(bullet: EnemyBullet, blocks: list[BunkerBlock]) -> Optional[BunkerBlock]:
    touched_blocks = [block for block in blocks if bullet_path_intersects_block(bullet, block)]
    if not touched_blocks:
        return None
    return min(touched_blocks, key=lambda block: block.y)


def bullet_path_intersects_block(bullet: EnemyBullet, block: BunkerBlock) -> bool:
    bullet_left = bullet.x - BUNKER_HIT_PADDING
    bullet_right = bullet.right + BUNKER_HIT_PADDING
    path_top = min(bullet.previous_y, bullet.y)
    path_bottom = max(bullet.previous_bottom, bullet.bottom)

    return (
        bullet_left < block.right
        and bullet_right > block.x
        and path_top < block.bottom
        and path_bottom > block.y
    )


def damage_blocks_near_hit(hit_block: BunkerBlock, blocks: list[BunkerBlock]) -> None:
    hit_center_x = hit_block.x + hit_block.size / 2
    hit_center_y = hit_block.y + hit_block.size / 2
    for block in blocks:
        block_center_x = block.x + block.size / 2
        block_center_y = block.y + block.size / 2
        if abs(block_center_x - hit_center_x) <= BUNKER_DAMAGE_RADIUS and abs(block_center_y - hit_center_y) <= BUNKER_DAMAGE_RADIUS:
            block.damage()
