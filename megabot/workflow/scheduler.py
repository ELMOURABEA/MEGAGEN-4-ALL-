"""
Task scheduler for multi-tasking operations
"""
import asyncio
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
from ..database.storage import DatabaseStorage


class TaskScheduler:
    """Manages concurrent task execution with priority queues"""
    
    def __init__(self, max_concurrent_tasks: int, storage: DatabaseStorage):
        """
        Initialize task scheduler
        
        Args:
            max_concurrent_tasks: Maximum number of concurrent tasks
            storage: Database storage instance
        """
        self.max_concurrent_tasks = max_concurrent_tasks
        self.storage = storage
        self.active_tasks: Dict[int, asyncio.Task] = {}
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.running = False
    
    async def start(self):
        """Start the task scheduler"""
        self.running = True
        
        # Create worker tasks
        workers = [
            asyncio.create_task(self._worker(i))
            for i in range(self.max_concurrent_tasks)
        ]
        
        # Wait for all workers to complete
        await asyncio.gather(*workers)
    
    async def stop(self):
        """Stop the task scheduler"""
        self.running = False
        
        # Cancel all active tasks
        for task_id, task in self.active_tasks.items():
            task.cancel()
        
        self.active_tasks.clear()
    
    async def _worker(self, worker_id: int):
        """Worker coroutine that processes tasks from queue"""
        while self.running:
            try:
                # Get task from queue with timeout
                task_info = await asyncio.wait_for(
                    self.task_queue.get(),
                    timeout=1.0
                )
                
                task_id = task_info["id"]
                task_func = task_info["func"]
                task_args = task_info["args"]
                task_kwargs = task_info["kwargs"]
                
                # Update task status
                self.storage.update_task(task_id, "running")
                
                try:
                    # Execute the task
                    result = await task_func(*task_args, **task_kwargs)
                    
                    # Update task with result
                    self.storage.update_task(task_id, "completed", str(result))
                    
                except Exception as e:
                    # Update task with error
                    self.storage.update_task(task_id, "failed", str(e))
                
                finally:
                    # Mark task as done
                    self.task_queue.task_done()
                    
            except asyncio.TimeoutError:
                # No task available, continue waiting
                continue
            except Exception as e:
                print(f"Worker {worker_id} error: {e}")
    
    async def schedule_task(
        self,
        task_name: str,
        task_func: Callable,
        priority: int = 1,
        *args,
        **kwargs
    ) -> int:
        """
        Schedule a new task
        
        Args:
            task_name: Name of the task
            task_func: Async function to execute
            priority: Task priority (higher = more important)
            *args: Positional arguments for task_func
            **kwargs: Keyword arguments for task_func
            
        Returns:
            Task ID
        """
        # Create task in database
        task_id = self.storage.create_task(task_name, priority)
        
        # Add to queue
        await self.task_queue.put({
            "id": task_id,
            "name": task_name,
            "func": task_func,
            "args": args,
            "kwargs": kwargs,
            "priority": priority
        })
        
        return task_id
    
    def get_task_status(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        # Query from database
        # This is a simplified version
        return {"id": task_id, "status": "querying from database"}
    
    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get all pending tasks"""
        return self.storage.get_pending_tasks()
    
    async def execute_immediate(self, task_func: Callable, *args, **kwargs) -> Any:
        """
        Execute a task immediately without queuing
        
        Args:
            task_func: Async function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Task result
        """
        return await task_func(*args, **kwargs)
