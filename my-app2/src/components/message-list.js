import React from 'react';
import { Card, CardContent } from '../ui/card';
import { Avatar, AvatarFallback } from '../ui/avatar';
import { Scale, User } from 'lucide-react';
import { cn } from '../lib/utils';

export function MessageList({ messages, isLoading }) {
  return (
    <div className="space-y-4">
      {messages.map((message) => (
        <div key={message.id} className={cn('flex gap-3', message.role === 'user' ? 'justify-end' : 'justify-start')}>
          {message.role === 'assistant' && (
            <Avatar className="h-8 w-8 bg-blue-600">
              <AvatarFallback>
                <Scale className="h-4 w-4 text-white" />
              </AvatarFallback>
            </Avatar>
          )}
          <Card className={cn('max-w-[80%]', message.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700')}>
            <CardContent className="p-4">
              <div className="prose prose-sm max-w-none">
                {message.content.split('\n').map((line, index) => (
                  <p key={index} className={cn('mb-2 last:mb-0', message.role === 'user' ? 'text-white' : 'text-gray-900 dark:text-gray-100')}>
                    {line}
                  </p>
                ))}
              </div>
            </CardContent>
          </Card>
          {message.role === 'user' && (
            <Avatar className="h-8 w-8 bg-gray-600">
              <AvatarFallback>
                <User className="h-4 w-4 text-white" />
              </AvatarFallback>
            </Avatar>
          )}
        </div>
      ))}
      {isLoading && (
        <div className="flex gap-3 justify-start">
          <Avatar className="h-8 w-8 bg-blue-600">
            <AvatarFallback>
              <Scale className="h-4 w-4 text-white" />
            </AvatarFallback>
          </Avatar>
          <Card className="bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700">
            <CardContent className="p-4">
              <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400">
                <span className="h-4 w-4 animate-spin">...</span>
                <span className="text-sm">Analyzing document...</span>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
} 