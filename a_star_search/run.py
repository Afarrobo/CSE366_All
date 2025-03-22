import pygame
import sys
from agent import Agent
from environment import Environment


WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRID_SIZE = 40
STATUS_WIDTH = 200
BACKGROUND_COLOR = (255, 255, 255)
BARRIER_COLOR = (0, 0, 0)       
TASK_COLOR = (255, 0, 0)       
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)

def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH + STATUS_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame AI Grid Simulation")

    
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

   
    environment = Environment(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, num_tasks=5, num_barriers=15)
    agent = Agent(environment, GRID_SIZE)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(agent)

    
    button_width, button_height = 100, 50
    button_x = WINDOW_WIDTH + (STATUS_WIDTH - button_width) // 2
    button_y = WINDOW_HEIGHT // 2 - button_height // 2
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    simulation_started = False

    
    last_move_time = 0
    MOVEMENT_DELAY = 200  
    
    
    running = True
    while running:
        clock.tick(60)  

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not simulation_started and event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    simulation_started = True
                    
                    if environment.task_locations:
                        agent.find_nearest_task()

        
        screen.fill(BACKGROUND_COLOR)

        
        for x in range(environment.columns):
            for y in range(environment.rows):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Draw grid lines

       
        for (bx, by) in environment.barrier_locations:
            barrier_rect = pygame.Rect(bx * GRID_SIZE, by * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BARRIER_COLOR, barrier_rect)

        
        for (tx, ty), task_number in environment.task_locations.items():
            task_rect = pygame.Rect(tx * GRID_SIZE, ty * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, TASK_COLOR, task_rect)
            task_num_surface = font.render(str(task_number), True, (255, 255, 255))
            task_num_rect = task_num_surface.get_rect(center=task_rect.center)
            screen.blit(task_num_surface, task_num_rect)

        
        all_sprites.draw(screen)

        
        current_time = pygame.time.get_ticks()
        if simulation_started and agent.moving and (current_time - last_move_time > MOVEMENT_DELAY):
            agent.move()
            last_move_time = current_time  

        
        status_x = WINDOW_WIDTH + 10
        algorithm_text = "Algorithm: A* Search"
        task_status_text = f"Tasks Completed: {agent.task_completed}"
        position_text = f"Position: {agent.position}"
        completed_tasks_text = f"Completed Tasks: {agent.completed_tasks}"
        total_cost_text = f"Total Path Cost: {agent.total_path_cost}"

        
        algorithm_surface = font.render(algorithm_text, True, TEXT_COLOR)
        task_status_surface = font.render(task_status_text, True, TEXT_COLOR)
        position_surface = font.render(position_text, True, TEXT_COLOR)
        completed_tasks_surface = font.render(completed_tasks_text, True, TEXT_COLOR)
        total_cost_surface = font.render(total_cost_text, True, TEXT_COLOR)

        
        screen.blit(algorithm_surface, (status_x, 20))
        screen.blit(task_status_surface, (status_x, 50))
        screen.blit(position_surface, (status_x, 80))
        screen.blit(completed_tasks_surface, (status_x, 110))
        screen.blit(total_cost_surface, (status_x, 140))

        
        if not simulation_started:
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
            button_text_surface = font.render("Start", True, BUTTON_TEXT_COLOR)
            button_text_rect = button_text_surface.get_rect(center=button_rect.center)
            screen.blit(button_text_surface, button_text_rect)
        
        pygame.display.flip()  

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()