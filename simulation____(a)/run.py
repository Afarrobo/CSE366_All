# run.py
import pygame
import sys
from agent import Agent
from environment import Environment

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRID_SIZE = 40
STATUS_WIDTH = 200
BACKGROUND_COLOR = (255, 255, 255)
BARRIER_COLOR = (0, 0, 0)       # Barrier color is black
TASK_COLOR = (255, 0, 0)        # Task color changed to red
TEXT_COLOR = (0, 0, 0)
MOVEMENT_DELAY = 200  # Milliseconds between movements

def main():
    pygame.init()

    # Set up display with an additional status panel
    screen = pygame.display.set_mode((WINDOW_WIDTH + STATUS_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame AI Grid Simulation")

    # Clock to control frame rate
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Initialize environment and agent
    environment = Environment(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, num_tasks=3, num_barriers=10)
    agent = Agent(environment, GRID_SIZE)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(agent)

    # Variables for movement delay
    last_move_time = pygame.time.get_ticks()

    # Main loop
    running = True
    while running:
        clock.tick(60)  # Limit to 60 FPS

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get key presses for movement
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if current_time - last_move_time > MOVEMENT_DELAY:
            if keys[pygame.K_UP]:
                agent.move("up")
                last_move_time = current_time
            elif keys[pygame.K_DOWN]:
                agent.move("down")
                last_move_time = current_time
            elif keys[pygame.K_LEFT]:
                agent.move("left")
                last_move_time = current_time
            elif keys[pygame.K_RIGHT]:
                agent.move("right")
                last_move_time = current_time

            # Check if the agent reached a task location
            agent.check_task_completion()

        # Draw grid and barriers
        screen.fill(BACKGROUND_COLOR)
        for x in range(environment.columns):
            for y in range(environment.rows):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Draw grid lines

        # Draw barriers
        for (bx, by) in environment.barrier_locations:
            barrier_rect = pygame.Rect(bx * GRID_SIZE, by * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BARRIER_COLOR, barrier_rect)

        # Draw tasks with numbers
        for (tx, ty), task_number in environment.task_locations.items():
            task_rect = pygame.Rect(tx * GRID_SIZE, ty * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, TASK_COLOR, task_rect)
            # Draw task number
            task_num_surface = font.render(str(task_number), True, (255, 255, 255))
            task_num_rect = task_num_surface.get_rect(center=task_rect.center)
            screen.blit(task_num_surface, task_num_rect)

        # Draw agent
        all_sprites.draw(screen)

        # Display status panel
        status_x = WINDOW_WIDTH + 10
        task_status_text = f"Tasks Completed: {agent.task_completed}"
        position_text = f"Position: {agent.position}"
        completed_tasks_text = f"Completed Tasks: {agent.completed_tasks}"
        status_surface = font.render(task_status_text, True, TEXT_COLOR)
        position_surface = font.render(position_text, True, TEXT_COLOR)
        completed_tasks_surface = font.render(completed_tasks_text, True, TEXT_COLOR)

        screen.blit(status_surface, (status_x, 20))
        screen.blit(position_surface, (status_x, 50))
        screen.blit(completed_tasks_surface, (status_x, 80))

        # Update the display
        pygame.display.flip()

    # Quit Pygame properly
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()